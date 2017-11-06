# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/23722012.py generated: Fri, 03 Nov 2017 08:48:41
#
# Event Type: 23722012
#
# ASCII decay Descriptor: [D_s+ --> (phi(1020) ==> e- e+) ...]CC
#
from Configurables import Generation
Generation().EventType = 23722012
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Ds_phiX,ee=DecProdCut.dec"
Generation().SignalPlain.CutTool = "DaughtersInLHCb"
Generation().SignalPlain.SignalPIDList = [ 431,-431 ]