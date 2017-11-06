# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/21113036.py generated: Fri, 03 Nov 2017 08:48:39
#
# Event Type: 21113036
#
# ASCII decay Descriptor: [D+ -> pi- e+ mu+]cc
#
from Configurables import Generation
Generation().EventType = 21113036
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/D+_pi-emu=DecProdCut.dec"
Generation().SignalPlain.CutTool = "DaughtersInLHCb"
Generation().SignalPlain.SignalPIDList = [ 411,-411 ]