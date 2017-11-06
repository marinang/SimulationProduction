# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/11364423.py generated: Fri, 03 Nov 2017 08:48:40
#
# Event Type: 11364423
#
# ASCII decay Descriptor: {[[B0]nos -> (D*(2007)~0 -> {(D~0 -> K+ K-) (pi0 -> gamma gamma), (D~0 -> K+ K-) gamma} ) K+ K- ]cc, [[B0]os -> (D*(2007)0 -> {(D0 -> K- K+) (pi0 -> gamma gamma), (D0 -> K- K+) gamma} ) K- K+ ]cc}
#
from Configurables import Generation
Generation().EventType = 11364423
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bd_Dst0KK,D0,KK=sqDalitz,DecProdCut.dec"
Generation().SignalRepeatedHadronization.CutTool = "DaughtersInLHCb"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 511,-511 ]