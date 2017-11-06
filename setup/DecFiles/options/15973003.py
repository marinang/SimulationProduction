# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/15973003.py generated: Fri, 03 Nov 2017 08:48:47
#
# Event Type: 15973003
#
# ASCII decay Descriptor: [Lambda_b0 -> (Lambda_c(2593)+ -> (Sigma_c0 -> MyLambda_c+ pi-) pi+) tau- anti-nu_tau]cc
#
from Configurables import Generation
Generation().EventType = 15973003
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Lb_Lc2593taunu,Sigmacpi,Lcpi=DecProdCut.dec"
Generation().SignalPlain.CutTool = "DaughtersInLHCb"
Generation().SignalPlain.SignalPIDList = [ 5122,-5122 ]