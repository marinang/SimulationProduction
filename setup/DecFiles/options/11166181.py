# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/11166181.py generated: Fri, 03 Nov 2017 08:48:43
#
# Event Type: 11166181
#
# ASCII decay Descriptor: [B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi- ) (K*(892)+ -> (KS0 -> pi+ pi-) pi+)]cc
#
from Configurables import Generation
Generation().EventType = 11166181
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bd_DstKst,D0pi,Kspi=DecProdCut,HELAMP001.dec"
Generation().SignalRepeatedHadronization.CutTool = "DaughtersInLHCb"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 511,-511 ]