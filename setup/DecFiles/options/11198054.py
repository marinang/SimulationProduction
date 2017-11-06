# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/11198054.py generated: Fri, 03 Nov 2017 08:48:50
#
# Event Type: 11198054
#
# ASCII decay Descriptor: [B0 -> D*(2010)- (D0 -> K- pi+ pi+ pi-) K+]cc
#
from Configurables import Generation
Generation().EventType = 11198054
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bd_DstD0K,D0pi_Kpi,K3pi=sqDalitz23,DecProdCut.dec"
Generation().SignalRepeatedHadronization.CutTool = "DaughtersInLHCb"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 511,-511 ]