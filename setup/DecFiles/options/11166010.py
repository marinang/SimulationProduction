# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/11166010.py generated: Fri, 03 Nov 2017 08:48:44
#
# Event Type: 11166010
#
# ASCII decay Descriptor: {[[B0]nos -> (D- => K+ pi- pi-) (a_1(1260)+ -> pi+ (rho(770)0 -> pi+ pi-))]cc, [[B0]os -> (D+ => K- pi+ pi+) (a_1(1260)- -> pi- (rho(770)0 -> pi- pi+))]cc}
#
from Configurables import Generation
Generation().EventType = 11166010
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bd_D-a1+,D0pi-.dec"
Generation().SignalRepeatedHadronization.CutTool = "LHCbAcceptance"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 511,-511 ]