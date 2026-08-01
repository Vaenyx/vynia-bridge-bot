use poise::serenity_prelude as serenity;

use crate::apis::urchin::UrchinApi;
use crate::config::DiscordConfig;
use crate::discord::{Data, Error, commands};

pub async fn start_discord_bot(config: DiscordConfig, urchin_api: UrchinApi) -> Result<(), Error> {
    let token = config.token;

    let options = poise::FrameworkOptions {
        commands: vec![
            commands::ping(),
            commands::bwsession(),
            commands::daily(),
            commands::weekly(),
            commands::monthly(),
            commands::yearly(),
        ],
        ..Default::default()
    };

    let framework = poise::Framework::builder()
        .options(options)
        .setup(move |ctx, _ready, framework| {
            let urchin_api = urchin_api.clone();

                Box::pin(async move {
                poise::builtins::register_globally(
                    ctx,
                    &framework.options().commands,
                )
                .await?;

                Ok(Data { urchin: urchin_api })
            })
        })
        .build();

    let intents = serenity::GatewayIntents::non_privileged();

    let mut client = serenity::ClientBuilder::new(token, intents)
        .framework(framework)
        .await?;

    client.start().await?;

    return Ok(());
}
