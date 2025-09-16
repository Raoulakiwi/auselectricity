// Data source URLs and information
export const DATA_SOURCES = {
  electricity: {
    aemo: {
      name: "Australian Energy Market Operator (AEMO)",
      url: "https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem",
      description: "Official NEM data dashboard - Real-time electricity prices and market data"
    },
    opennem: {
      name: "OpenNEM",
      url: "https://opennem.org.au/",
      description: "Open source National Electricity Market data"
    },
    nemosis: {
      name: "NEMOSIS",
      url: "https://github.com/UNSW-CEEM/NEMOSIS",
      description: "Python package for accessing AEMO data"
    }
  },
  dams: {
    waternsw: {
      name: "WaterNSW",
      url: "https://www.waternsw.com.au/water-services/water-data",
      description: "New South Wales dam levels and water storage information"
    },
    melbourne_water: {
      name: "Melbourne Water",
      url: "https://www.melbournewater.com.au/water/water-storage-levels",
      description: "Victoria water storage levels and dam information"
    },
    seqwater: {
      name: "Seqwater",
      url: "https://www.seqwater.com.au/dam-levels",
      description: "Queensland dam levels and water storage data"
    },
    sawater: {
      name: "SA Water (WaterConnect)",
      url: "https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx",
      description: "South Australia real-time water data and reservoir levels"
    },
    hydrotasmania: {
      name: "Hydro Tasmania",
      url: "https://www.hydro.com.au/water/lake-levels",
      description: "Tasmania hydroelectric dams and lake levels"
    }
  }
};

// Specific dam URLs mapping
export const SPECIFIC_DAM_URLS = {
  // Queensland (Seqwater)
  'Burdekin Falls': 'https://www.seqwater.com.au/dams/burdekin-falls',
  'Fairbairn': 'https://www.seqwater.com.au/dams/fairbairn',
  'Hinze': 'https://www.seqwater.com.au/dams/hinze',
  'Somerset': 'https://www.seqwater.com.au/dams/somerset',
  'Wivenhoe': 'https://www.seqwater.com.au/dams/wivenhoe',
  'Baroon Pocket': 'https://www.seqwater.com.au/dams/baroon-pocket',
  'Borumba': 'https://www.seqwater.com.au/dams/borumba',
  'Cooloolabin': 'https://www.seqwater.com.au/dams/cooloolabin',
  'Ewen Maddock': 'https://www.seqwater.com.au/dams/ewen-maddock',
  'Lake Macdonald': 'https://www.seqwater.com.au/dams/lake-macdonald',
  'Lake Manchester': 'https://www.seqwater.com.au/dams/lake-manchester',
  'Leslie Harrison': 'https://www.seqwater.com.au/dams/leslie-harrison',
  'Little Nerang': 'https://www.seqwater.com.au/dams/little-nerang',
  'Maroon': 'https://www.seqwater.com.au/dams/maroon',
  'Moogerah': 'https://www.seqwater.com.au/dams/moogerah',
  'North Pine': 'https://www.seqwater.com.au/dams/north-pine',
  'Poona': 'https://www.seqwater.com.au/dams/poona',
  'Sideling Creek': 'https://www.seqwater.com.au/dams/sideling-creek',
  'Six Mile Creek': 'https://www.seqwater.com.au/dams/six-mile-creek',
  'Tingalpa': 'https://www.seqwater.com.au/dams/tingalpa',
  'Wappa': 'https://www.seqwater.com.au/dams/wappa',
  
  // New South Wales (WaterNSW) - using general dam levels page for now
  'Blowering': 'https://www.waternsw.com.au/supply/dam-levels',
  'Burrinjuck': 'https://www.waternsw.com.au/supply/dam-levels',
  'Copeton': 'https://www.waternsw.com.au/supply/dam-levels',
  'Eucumbene': 'https://www.waternsw.com.au/supply/dam-levels',
  'Warragamba': 'https://www.waternsw.com.au/supply/dam-levels',
  'Windamere': 'https://www.waternsw.com.au/supply/dam-levels',
  
  // Victoria (Melbourne Water) - using general dam levels page for now
  'Dartmouth': 'https://www.melbournewater.com.au/water/water-storage-levels',
  'Eildon': 'https://www.melbournewater.com.au/water/water-storage-levels',
  'Hume': 'https://www.melbournewater.com.au/water/water-storage-levels',
  'Thomson': 'https://www.melbournewater.com.au/water/water-storage-levels',
  'Yarrawonga': 'https://www.melbournewater.com.au/water/water-storage-levels',
  
  // South Australia (SA Water) - using WaterConnect real-time data
  'Happy Valley': 'https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx',
  'Mount Bold': 'https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx',
  'Myponga': 'https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx',
  
  // Tasmania (Hydro Tasmania) - using specific lake data files
  'Gordon': 'https://www.hydro.com.au/water/lake-levels/GetLakeLevelDataFile?filename=Web%5FLakes%5FGORDON.pdf',
  'Great Lake': 'https://www.hydro.com.au/water/lake-levels/GetLakeLevelDataFile?filename=Web%5FLakes%5FGREAT.pdf',
  'Lake Pedder': 'https://www.hydro.com.au/water/lake-levels/GetLakeLevelDataFile?filename=Web%5FLakes%5FPEDDER.pdf'
};

// Helper function to get source info for a region/state
export const getSourceInfo = (type, region) => {
  if (type === 'electricity') {
    // For electricity, we use AEMO as the primary source
    return DATA_SOURCES.electricity.aemo;
  } else if (type === 'dams') {
    // For dams, map states to their primary water authority
    const stateMapping = {
      'NSW': DATA_SOURCES.dams.waternsw,
      'VIC': DATA_SOURCES.dams.melbourne_water,
      'QLD': DATA_SOURCES.dams.seqwater,
      'SA': DATA_SOURCES.dams.sawater,
      'TAS': DATA_SOURCES.dams.hydrotasmania
    };
    return stateMapping[region] || DATA_SOURCES.dams.waternsw;
  }
  return null;
};

// Helper function to get specific dam URL
export const getDamUrl = (damName) => {
  return SPECIFIC_DAM_URLS[damName] || null;
};

// Helper function to get all sources for a type
export const getAllSources = (type) => {
  return Object.values(DATA_SOURCES[type] || {});
};
