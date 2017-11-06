# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/11100013.py generated: Fri, 03 Nov 2017 08:48:42
#
# Event Type: 11100013
#
# ASCII decay Descriptor: [B_0 -> (tau+ -> pi+ pi- pi+ anti-nu_tau) (tau- -> pi+ pi- pi- nu_tau)]cc
#
from Gaudi.Configuration import *
importOptions( "$DECFILESROOT/options/B2XTau.py" )
from Configurables import Generation
Generation().EventType = 11100013
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bd_tautau,pipipinu=DecProdCut,TightCut,tauolacleointricate.dec"
Generation().SignalRepeatedHadronization.CutTool = "DaughtersInLHCbAndWithDaughAndBCuts"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 511,-511 ]