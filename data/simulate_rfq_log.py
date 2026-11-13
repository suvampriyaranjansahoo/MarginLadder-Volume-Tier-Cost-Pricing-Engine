import random, csv, statistics as st
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
random.seed(2611)
# ASSUMED mean days per stage (illustration, assumption A5). Costing is from the brief: 12.5 h / 8 h = 1.56 days.
means={"Intake wait":1.5,"Costing":1.56,"Routing check wait":1.9,"Approval wait":2.4,"Send and rework":1.64}
N=60; rows=[]
raw={k:[random.lognormvariate(0,0.55) for _ in range(N)] for k in means}
for k in means:
    f=means[k]/st.mean(raw[k]); raw[k]=[round(x*f,2) for x in raw[k]]
for i in range(N):
    d={k:raw[k][i] for k in means}; d["RFQ"]=f"SIM-{i+1:03d}"; d["Total days"]=round(sum(raw[k][i] for k in means),2); rows.append(d)
cols=["RFQ"]+list(means)+["Total days"]
with open("simulated_rfq_log.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
tot=[r["Total days"] for r in rows]
m={k:st.mean(r[k] for r in rows) for k in means}
print({k:round(v,2) for k,v in m.items()}, round(st.mean(tot),2), "median",round(st.median(tot),2),"<=4d",sum(t<=4 for t in tot),"max",max(tot))
fig,ax=plt.subplots(1,2,figsize=(13,4.6),dpi=160)
cl=["#c0564a","#0f5c5c","#d88c4a","#7a5c9e","#41585a"]
left=0
for (k,v),c in zip(m.items(),cl):
    ax[0].barh(["Mean RFQ"],[v],left=left,color=c,label=f"{k} {v:.2f}"); ax[0].text(left+v/2,0,f"{v:.2f}",ha="center",va="center",color="#fff",fontsize=11,fontweight="bold"); left+=v
ax[0].set_xlim(0,9.5); ax[0].set_xlabel("Working days"); ax[0].legend(loc="upper center",bbox_to_anchor=(0.5,-0.25),ncol=3,fontsize=9,frameon=False)
ax[0].set_title("Where 9 days go (simulated)",fontsize=13,loc="left")
ax[1].hist(tot,bins=14,color="#0f5c5c"); ax[1].axvline(4,color="#c0564a",ls="--"); ax[1].text(4.1,ax[1].get_ylim()[1]*0.9,"4-day target",color="#c0564a")
ax[1].set_xlabel("Total working days per RFQ"); ax[1].set_ylabel("RFQs"); ax[1].set_title(f"Spread: median {st.median(tot):.1f}, {sum(t<=4 for t in tot)} of 60 within 4 days (simulated)",fontsize=13,loc="left")
fig.text(0.01,0.01,"SIMULATED from assumed stage means (A5). Costing 1.56 days is derived from the brief. The Week 1 trace of real RFQs replaces this.",fontsize=9,color="#41585a")
plt.tight_layout(rect=(0,0.04,1,1)); plt.savefig("../docs/ba/cycle_time_simulated.png")
