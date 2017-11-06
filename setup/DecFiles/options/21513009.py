# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/21513009.py generated: Fri, 03 Nov 2017 08:48:38
#
# Event Type: 21513009
#
# ASCII decay Descriptor: [D+ -> ( tau+ -> mu+ mu+ e- ) nu_tau ]cc
#
from Configurables import Generation
Generation().EventType = 21513009
Generation().SampleGenerationTool = "SignalPlain"
from Configurables import SignalPlain
Generation().addTool( SignalPlain )
Generation().SignalPlain.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/D+_taunu,mme=SS,FromB,TightCut.dec"
Generation().SignalPlain.CutTool = "LoKi::GenCutTool/TightCut"
Generation().SignalPlain.SignalPIDList = [ 411,-411 ]

# 
from Configurables import LoKi__GenCutTool 
gen = Generation() 
gen.SignalPlain.addTool ( LoKi__GenCutTool , 'TightCut' ) 
# 
tightCut = gen.SignalPlain.TightCut
tightCut.Decay     = '[ D+ -> ( ^(tau+ -> ^mu+ ^mu+ ^e-) ) nu_tau ]CC'
tightCut.Cuts      =    {
    '[e+]cc'  : ' goodElectron ' , 
    '[mu+]cc'  : ' goodMuon ' , 
    '[tau+]cc' : ' goodTau  ' }
tightCut.Preambulo += [
    'inAcc    = in_range ( 0.005 , GTHETA , 0.400 ) ' , 
    'goodElectron = ( GPT > 0.20 * GeV ) & ( GP > 2.0 * GeV ) & inAcc ' ,  
    'goodMuon = ( GPT > 0.20 * GeV ) & ( GP > 2.0 * GeV ) & inAcc ' , 
    'goodTau  = GHAS (GBEAUTY, HepMC.ancestors) ' ]

