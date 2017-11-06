# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/15144520.py generated: Fri, 03 Nov 2017 08:48:39
#
# Event Type: 15144520
#
# ASCII decay Descriptor: [Lambda_b0 -> (Lambda0 -> p+ pi-) (J/psi(1S) -> mu+ mu- ) (pi0 -> gamma gamma)]cc
#
from Configurables import Generation
Generation().EventType = 15144520
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Lb_JpsiLambdapi0,mm=phsp,DecProdCut.dec"
Generation().SignalPlain.CutTool = "DaughtersInLHCb"
Generation().SignalPlain.SignalPIDList = [ 5122,-5122 ]