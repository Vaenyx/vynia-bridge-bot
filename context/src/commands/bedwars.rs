use humantime::parse_duration;

use crate::apis::urchin::{CustomSession, SessionResponse, UrchinApi};
use crate::error::Result;

pub async fn get_bw_custom_stats(
    urchin: &UrchinApi,
    username: &str,
    session: CustomSession,
) -> Result<SessionResponse> {
    let session = match session {
        CustomSession::Duration(duration) => {
            let hours = parse_duration(&duration)?.as_secs() / 60 / 60;

            if hours > 200_000 {
                anyhow::bail!("Duration too large. Max is 200000h.");
            }

            CustomSession::Duration(format!("{hours}h"))
        }

        CustomSession::FromMs(from_ms) => CustomSession::FromMs(from_ms),
    };

    let stats = urchin.get_custom_stats(username, session).await?;
    return Ok(stats);
}
