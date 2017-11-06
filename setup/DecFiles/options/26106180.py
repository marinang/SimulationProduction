# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/26106180.py generated: Fri, 03 Nov 2017 08:48:40
#
# Event Type: 26106180
#
# ASCII decay Descriptor: [Xi_c0 -> (Xi- -> (Lambda0 -> p+ pi-) pi-) pi+ pi- pi+]cc
#
from Configurables import Generation
Generation().EventType = 26106180
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Xic_Xipipipi,Lambdapi=DecProdCut.dec"
Generation().SignalPlain.CutTool = "DaughtersInLHCb"
Generation().SignalPlain.SignalPIDList = [ 4132,-4132 ]