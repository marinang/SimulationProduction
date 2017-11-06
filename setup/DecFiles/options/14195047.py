# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/14195047.py generated: Fri, 03 Nov 2017 08:48:43
#
# Event Type: 14195047
#
# ASCII decay Descriptor: [B_c+ -> (D+ -> pi+ K- pi+) (anti-D0 -> K+ pi-)]cc
#
from Configurables import Generation
Generation().EventType = 14195047
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "BcVegPyProduction"
Generation().PileUpTool = "FixedLuminosityForRareProcess"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bc_D0D,Kpi,piKpi=DDalitz,BcVegPy,DecProdCut.dec"
Generation().Special.CutTool = "BcDaughtersInLHCb"