use serde::Deserialize;

#[derive(Debug, Clone)]
pub enum CustomSession {
    Duration(String),
    FromMs(i64),
}

#[derive(Debug, Clone, Copy)]
pub enum Period {
    Daily,
    Weekly,
    Monthly,
    Yearly,
}

impl Period {
    pub fn label(&self) -> &'static str {
        match self {
            Period::Daily => "Daily",
            Period::Weekly => "Weekly",
            Period::Monthly => "Monthly",
            Period::Yearly => "Yearly",
        }
    }

    pub fn as_hours(&self) -> u32 {
        match self {
            Period::Daily => 24,
            Period::Weekly => 168,
            Period::Monthly => 720,
            Period::Yearly => 8760,
        }
    }
}

#[derive(Debug, Deserialize)]
pub struct SessionResponse {
    pub uuid: String,
    pub displayname: String,
    pub from: i64,
    pub from_readable: String,
    pub delta: Delta,
}

#[derive(Debug, Deserialize)]
pub struct Delta {
    pub stats: Stats,
}

#[derive(Debug, Deserialize)]
pub struct Stats {
    #[serde(rename = "Bedwars")]
    pub bedwars: BedwarsStats,
}

#[derive(Debug, Deserialize)]
pub struct BedwarsStats {
    #[serde(default)]
    pub wins_bedwars: u32,

    #[serde(default)]
    pub losses_bedwars: u32,

    #[serde(default)]
    pub final_kills_bedwars: u32,

    #[serde(default)]
    pub final_deaths_bedwars: u32,

    #[serde(default)]
    pub kills_bedwars: u32,

    #[serde(default)]
    pub deaths_bedwars: u32,

    #[serde(default)]
    pub beds_broken_bedwars: u32,

    #[serde(default)]
    pub beds_lost_bedwars: u32,

    #[serde(default)]
    pub games_played_bedwars: u32,

    #[serde(default, rename = "Experience")]
    pub experience: u32,
}
