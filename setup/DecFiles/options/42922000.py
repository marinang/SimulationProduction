# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/42922000.py generated: Fri, 03 Nov 2017 08:48:43
#
# Event Type: 42922000
#
# ASCII decay Descriptor: pp -> (Z-> el el) (b b~)...
#
from Configurables import Generation
Generation().EventType = 42922000
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Z_eebb_AlpGen.dec"
Generation().Special.CutTool = ""

Generation.AlpGenDict = {
'alpgen_nevxiter' : 100000,
'alpgen_niter' : 2,
'alpgen_nwgtev' : 1000000,
'alpgen_FileLabel' : "zbb",
'alpgen_njets' : 0, #number of light jets
'alpgen_etabmin' : 1.596,
'alpgen_ptbmin' : 3.0,
'alpgen_drbmin' : 0.1,
'alpgen_etabmax' : 10.0,
'alpgen_eta1lmin' : 1.596,
'alpgen_ptlmin' : 10.0,
'alpgen_drlmin' : 0.,
'alpgen_etalmax' : 10.0,
'alpgen_izdecmode' : 1,
'alpgen_ndns' : 9,
}

