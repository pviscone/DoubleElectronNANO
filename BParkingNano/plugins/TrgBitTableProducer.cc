//// table to produce hlt and l1 bits that we are going to use in the analysis, to avoid saving every bit in the menu


// system include files
#include <memory>

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"


#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "TString.h"
#include <string>

#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"



class TrgBitTableProducer : public edm::stream::EDProducer<> {


public:

 
 explicit TrgBitTableProducer(const edm::ParameterSet &cfg):
    l1GtMenuToken_(esConsumes<L1TUtmTriggerMenu, L1TUtmTriggerMenuRcd>()),
    hltresultsToken_(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag> ("hltresults"))),
    l1resultsToken_(consumes<GlobalAlgBlkBxCollection>(cfg.getParameter<edm::InputTag> ("l1results"))),
    hltpaths_( cfg.getParameter< std::vector<std::string> >( "paths" ) ),
    l1seeds_( cfg.getParameter< std::vector<std::string> >( "seeds" ) )
{
    produces<nanoaod::FlatTable>();
    // produces<nanoaod::FlatTable>("globalVariables");

}

  ~TrgBitTableProducer() override {}

  void produce(edm::Event&, edm::EventSetup const&) override;


  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions) {}
  

private:

  const edm::ESGetToken<L1TUtmTriggerMenu, L1TUtmTriggerMenuRcd> l1GtMenuToken_;
  const edm::EDGetTokenT< edm::TriggerResults >    hltresultsToken_;
  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1resultsToken_;
  // l1 seeds not implemented yet but can be added with litle effort
  const std::vector< std::string >                 hltpaths_;
  const std::vector< std::string >                 l1seeds_;
  TString * algoBitToName  =  new TString[512]; 
  bool loaded = false;
};



void 
TrgBitTableProducer::produce( edm::Event &evt, edm::EventSetup const &stp) 
{

  //input
  edm::Handle<GlobalAlgBlkBxCollection> l1Results;
  evt.getByToken(l1resultsToken_,l1Results);
  edm::Handle< edm::TriggerResults > hltResults;
  evt.getByToken( hltresultsToken_, hltResults);


  // returns uint8 instead of bool, because addCollumnValue<bool> is unsuported. (cmsRun error). the next "economical" class is uint8
  std::vector<uint8_t> hltbits;
  std::vector<uint8_t> l1bits;
  unsigned int Npaths = hltpaths_.size();
  hltbits.reserve( Npaths );
  unsigned int Nseeds = l1seeds_.size();
  l1bits.reserve( Nseeds );
  edm::TriggerNames trigName = evt.triggerNames( *hltResults );   


 
  // get L1 seeds
  if ( !l1Results.isValid() ) {

   for (unsigned int iseed=0; iseed<l1seeds_.size(); iseed++)
     l1bits.push_back( 0 );

  } else{
    if (!loaded){
      const auto& menu = stp.getData(l1GtMenuToken_);
      for (auto const & keyval: menu.getAlgorithmMap()) {
        std::string const & trigName = keyval.second.getName();
        algoBitToName[ int( keyval.second.getIndex() ) ] = TString( trigName );
      }
      loaded=true;
    }

    GlobalAlgBlk const &result=l1Results->at(0, 0);
    for ( auto& l1seed: l1seeds_ ){
      bool sfire=false;
      for (unsigned int itrg=0; itrg<result.maxPhysicsTriggers; ++itrg){
        if (result.getAlgoDecisionFinal(itrg)!=1) continue;
        std::string l1trigName = static_cast<const char *>(algoBitToName[itrg]);
        if (l1trigName!=l1seed) continue;
        sfire=true;
        break;
    }
    if (sfire) l1bits.push_back( 1 );
    else l1bits.push_back( 0 );
    }
  }

  // get HLT triggers
  bool anyDoubleElefired_flag = false; // <--- NEW: Flag for DoubleEle HLT paths
  bool anyVBFfired_flag = false;       // <--- NEW: Flag for VBF HLT paths

  if ( hltResults.failedToGet() ){
    for ( unsigned int ibit = 0; ibit < Npaths; ++ibit)
      hltbits.push_back( 0 );

  } else {
    int Ntrg = hltResults->size();
    for ( auto& hltpath: hltpaths_ ){
      bool fire = false; 
      for( int itrg = 0; itrg < Ntrg; ++itrg ){
        if ( !hltResults->accept( itrg ) ) continue;
        TString TrigPath = trigName.triggerName( itrg );
        if ( TrigPath.Contains( hltpath ) ){
          fire=true;
          if (TrigPath.Contains("DoubleEle", TString::kIgnoreCase)) {
            anyDoubleElefired_flag = true;
          }
          if (TrigPath.Contains("VBF", TString::kIgnoreCase)) {
            anyVBFfired_flag = true;
          }
          break; 
        }
      } 
      
      if( fire ) hltbits.push_back( 1 );
      else hltbits.push_back( 0 );
    }
  }


  auto tab  = std::make_unique<nanoaod::FlatTable>(1,"", true, true);
  for (unsigned int ipath = 0; ipath <Npaths; ++ipath ){
    tab->addColumnValue<uint8_t> (hltpaths_[ipath], hltbits[ipath], "hlt path");
  }
  for (unsigned int iseed = 0; iseed <Nseeds; ++iseed ){
    tab->addColumnValue<uint8_t> (l1seeds_[iseed], l1bits[iseed], "l1 seed");
  }

  tab->addColumnValue<bool> ("any_DoubleEle_fired", anyDoubleElefired_flag, "1 if any of the configured HLT paths containing '_DoubleEle' fired"); // <--- NEW COLUMN
  tab->addColumnValue<bool> ("any_VBF_fired", anyVBFfired_flag, "1 if any of the configured HLT paths containing '_VBF_' fired");       // <--- NEW COLUMN

  evt.put(std::move(tab));

}


//define this as a plug-in
DEFINE_FWK_MODULE(TrgBitTableProducer);
