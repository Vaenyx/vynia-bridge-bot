use anyhow::Result;

mod apis;
mod commands;
mod config;
mod discord;
mod error;

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    let config = config::Config::from_env()?;

    let urchin_api = apis::urchin::UrchinApi::new(config.urchin.clone());

    let discord_task = discord::client::start_discord_bot(config.discord, urchin_api);

    // add new tasks for mc and such
    tokio::select! {
        discord_result = discord_task => {
            discord_result?;
        }
    }

    return Ok(());
}
