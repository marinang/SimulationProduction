# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/14297260.py generated: Fri, 03 Nov 2017 08:48:42
#
# Event Type: 14297260
#
# ASCII decay Descriptor: [ B_c+ => (D*(2010)+ => (D+ => K- pi+ pi+) gamma) (D~0 => K+ pi- pi+ pi-) ]cc
#
from Configurables import Generation
Generation().EventType = 14297260
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "BcVegPyProduction"
Generation().PileUpTool = "FixedLuminosityForRareProcess"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bc_DstD0,D+gamma,Kpipi,Kpipipi=BcVegPy,LooseNeutralCut,D0IncoherentSum.dec"
Generation().Special.CutTool = "BcDaughtersInLHCb"
from Configurables import BcDaughtersInLHCb
Generation().Special.addTool( BcDaughtersInLHCb )
Generation().Special.BcDaughtersInLHCb.NeutralThetaMin = 0.
Generation().Special.BcDaughtersInLHCb.NeutralThetaMax = 10.