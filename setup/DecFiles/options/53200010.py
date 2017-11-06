# file /home/marinang/GaussDev_v49r3/Gen/DecFiles/options/53200010.py generated: Fri, 03 Nov 2017 08:48:36
#
# Event Type: 53200000
#
# ASCII decay Descriptor: pi+,pi- => ?
#
from Configurables import ParticleGun
from Configurables import MomentumRange
ParticleGun().addTool( MomentumRange )
from GaudiKernel import SystemOfUnits
ParticleGun().MomentumRange.MomentumMin = 10.0*SystemOfUnits.GeV
from GaudiKernel import SystemOfUnits
ParticleGun().MomentumRange.MomentumMax = 10.0*SystemOfUnits.GeV
ParticleGun().EventType = 53200010
ParticleGun().ParticleGunTool = "MomentumRange"
ParticleGun().NumberOfParticlesTool = "FlatNParticles"
ParticleGun().MomentumRange.PdgCodes = [ 211, -211 ]
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/pi+pi-,fixP=CaloAcc.dec"
from Gaudi.Configuration import *
importOptions( "$DECFILESROOT/options/CaloAcceptance.py" )