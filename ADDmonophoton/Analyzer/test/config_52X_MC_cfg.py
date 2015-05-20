import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## global tag for data
process.GlobalTag.globaltag = cms.string('MC_52_V9::All')


from PhysicsTools.PatAlgos.tools.metTools import *                       
addPfMET(process,'PF')
addTcMET(process,"TC")       


# Select calo jets
process.patJetCorrFactors.levels = cms.vstring(['L1Offset','L2Relative','L3Absolute'])
process.selectedPatJets.cut = cms.string('pt > 10 & abs(eta) < 3.0')

# Add PF jets
from PhysicsTools.PatAlgos.tools.jetTools import *
addJetCollection(process,cms.InputTag('ak5PFJets'),
                 'AK5', 'PF',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF', cms.vstring(['L1FastJet','L2Relative','L3Absolute'])),
                 doType1MET    = True,
                 doL1Cleaning  = True,
                 doL1Counters  = False,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID       = False,
                 jetIdLabel    = "ak5"
                 )
process.selectedPatJetsAK5PF.cut = cms.string('pt > 10')



#fast jet 
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

process.kt6PFJets25 = process.kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJets25.Rho_EtaMax = cms.double(2.5)
process.kt6PFJets25.Ghost_EtaMax = cms.double(2.5)
process.fastjetSequence25 = cms.Sequence( process.kt6PFJets25 )
                 
process.kt6PFJets44 = process.kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJets44.Rho_EtaMax = cms.double(4.4)
process.kt6PFJets44.Ghost_EtaMax = cms.double(5.0) 
process.fastjetSequence44 = cms.Sequence( process.kt6PFJets44 )

process.load("RecoJets.JetProducers.ak5PFJets_cfi")
process.ak5PFJets.doAreaFastjet = True 




# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
readFiles.extend( [
  '/store/relval/CMSSW_5_2_2/RelValSingleGammaPt35/GEN-SIM-RECO/START52_V4-v2/0252/3086C457-E974-E111-8489-002354EF3BE0.root'       
    ] );

process.source = cms.Source("PoolSource",
    fileNames = readFiles
)

#closes files after code is done running on that file
process.options = cms.untracked.PSet(
	fileMode = cms.untracked.string('NOMERGE')
)

process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.demo = cms.EDAnalyzer('Analyzer',
                              electronTag      = cms.untracked.InputTag("selectedPatElectrons"),
                              tauTag           = cms.untracked.InputTag("selectedPatTaus"),
                              muonTag          = cms.untracked.InputTag("selectedPatMuons"),
                              cosMuonTag       = cms.untracked.InputTag("muonsFromCosmics"),
                              jetTag           = cms.untracked.InputTag("selectedPatJets"),
                              pfjetTag         = cms.untracked.InputTag("selectedPatJetsAK5PF"),
                              genjetTag        = cms.untracked.InputTag("ak5GenJets"),
                              photonTag        = cms.untracked.InputTag("selectedPatPhotons"),
                              uncleanphotonTag = cms.untracked.InputTag("selecteduncleanPatPhotons"),
                              caloTowerTag   = cms.untracked.InputTag("towerMaker"),
                              cscTag           = cms.untracked.InputTag("cscSegments"),
                              rpcTag           = cms.untracked.InputTag("rpcRecHits"),
                              rechitBTag       = cms.untracked.InputTag("reducedEcalRecHitsEB"),
                              rechitETag       = cms.untracked.InputTag("reducedEcalRecHitsEE"),
                              hcalrechitTag    = cms.untracked.InputTag("reducedHcalRecHits:hbhereco"),
                              metTag           = cms.untracked.InputTag("patMETs"),
                              PFmetTag         = cms.untracked.InputTag("patMETsPF"),
                              TCmetTag         = cms.untracked.InputTag("patMETsTC"),
                              HLTriggerResults = cms.untracked.InputTag("TriggerResults","","HLT"),#check what you need here HLT or REDIGI3..
                              triggerEventTag  = cms.untracked.InputTag("hltTriggerSummaryAOD","","HLT"),#check what you need here HLT or REDIGI3..
                              hltlabel          = cms.untracked.string("HLT"),   #check what you need here HLT or REDIGI3..
                              Tracks           = cms.untracked.InputTag("generalTracks"),
                              Vertices         = cms.untracked.InputTag("offlinePrimaryVertices","",""),
                              BeamHaloSummary  = cms.untracked.InputTag("BeamHaloSummary"),
                              pileup           = cms.untracked.InputTag("addPileupInfo"),
                              rhoLabel         = cms.untracked.InputTag("kt6PFJets25", "rho"),
                              sigmaLabel       = cms.untracked.InputTag("kt6PFJets25", "sigma"),
                              rhoLabel44         = cms.untracked.InputTag("kt6PFJets44", "rho"),
                              sigmaLabel44       = cms.untracked.InputTag("kt6PFJets44", "sigma"),
                              runphotons       = cms.untracked.bool(True),
                              rununcleanphotons= cms.untracked.bool(False),
                              runHErechit      = cms.untracked.bool(True),
                              runrechit        = cms.untracked.bool(True),
                              runmet           = cms.untracked.bool(True),
                              rungenmet        = cms.untracked.bool(True),
                              runPFmet         = cms.untracked.bool(True),
                              runTCmet         = cms.untracked.bool(True),
                              runjets          = cms.untracked.bool(True),
                              runpfjets        = cms.untracked.bool(True),
                              rungenjets        = cms.untracked.bool(True),
                              runelectrons     = cms.untracked.bool(True),
                              runtaus          = cms.untracked.bool(True),
                              runDetailTauInfo = cms.untracked.bool(True),
                              runmuons         = cms.untracked.bool(True),
                              runcosmicmuons   = cms.untracked.bool(True),
                              rungenParticleCandidates = cms.untracked.bool(False),
                              runHLT           = cms.untracked.bool(True),
                              runL1            = cms.untracked.bool(True),
                              runscraping      = cms.untracked.bool(False),
                              runtracks        = cms.untracked.bool(True),
                              runvertex        = cms.untracked.bool(True),
                              ##OFF for AOD---
                              runCSCseg        = cms.untracked.bool(False),
                              runRPChit        = cms.untracked.bool(False),
                              #---------------
                              runcaloTower     = cms.untracked.bool(True),
                              runBeamHaloSummary= cms.untracked.bool(True),
                              runPileUp         = cms.untracked.bool(True),
                              isAOD             = cms.untracked.bool(True),
                              debug            = cms.untracked.bool(False),
                              outFile          = cms.untracked.string('AOD_Output_G_Pt_120to170.root')
                              )





#All paths are here
process.p = cms.Path(
   process.fastjetSequence25*
   process.fastjetSequence44*
   process.ak5PFJets*
   process.patDefaultSequence*
   process.demo
   )


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)

# process all the events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.schedule=cms.Schedule(process.p)


