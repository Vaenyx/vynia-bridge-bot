use poise::serenity_prelude as serenity;

use crate::apis::urchin::UrchinApi;
use crate::config::DiscordConfig;
use crate::discord::{Data, Error, commands};

pub async fn start_discord_bot(config: DiscordConfig, urchin_api: UrchinApi) -> Result<(), Error> {
    let token = config.token;
    let guild_id = config.guild_id;

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
                poise::builtins::register_in_guild(
                    ctx,
                    &framework.options().commands,
                    serenity::GuildId::new(guild_id),
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
