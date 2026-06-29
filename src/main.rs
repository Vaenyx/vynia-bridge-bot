use anyhow::Result;

mod apis;
mod commands;
mod config;
mod discord;
mod error;

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    tracing_subscriber::fmt::init();

    let config = config::Config::from_env()?;
    let urchin_api = apis::urchin::UrchinApi::new(config.urchin.clone());

    discord::client::start_discord_bot(config.discord, urchin_api)
        .await
        .expect("Discord bot crashed at startup");

    return Ok(());
}
