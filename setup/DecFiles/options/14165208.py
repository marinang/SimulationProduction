# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/14165208.py generated: Fri, 03 Nov 2017 08:48:37
#
# Event Type: 14165208
#
# ASCII decay Descriptor: [B_c+ -> (D_s*+ -> (D_s+ -> pi+ pi- pi+) gamma) (phi(1020) -> K+ K-)]cc
#
from Configurables import Generation
Generation().EventType = 14165208
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "BcVegPyProduction"
Generation().PileUpTool = "FixedLuminosityForRareProcess"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bc_PhiDsst,KK,Dsgamma,pipipi=DecProdCut,BcVegPy,HELAMP100.dec"
Generation().Special.CutTool = "BcDaughtersInLHCb"