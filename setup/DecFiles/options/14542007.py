# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/14542007.py generated: Fri, 03 Nov 2017 08:48:39
#
# Event Type: 14542007
#
# ASCII decay Descriptor: [B_c+ => (J/psi(1S) => mu+ mu-) (tau+ ==> pi+ pi+ pi- nu_tau~) nu_tau]CC
#
from Configurables import Generation
Generation().EventType = 14542007
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "BcVegPyProduction"
Generation().PileUpTool = "FixedLuminosityForRareProcess"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bc_JpsiTauNu=BcVegPy,tauolacleo,DecProdCut.dec"
Generation().Special.CutTool = "BcDaughtersInLHCb"