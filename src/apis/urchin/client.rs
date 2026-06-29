use crate::config::UrchinConfig;
use crate::error::Result;

use super::types::{CustomSession, SessionResponse};

const URCHIN_BASE_URL: &str = "https://api.urchin.gg/v3";

#[derive(Clone)]
pub struct UrchinApi {
    client: reqwest::Client,
    api_key: String,
}

impl UrchinApi {
    pub fn new(config: UrchinConfig) -> Self {
        Self {
            client: reqwest::Client::new(),
            api_key: config.api_key,
        }
    }

    pub async fn get_custom_stats(
        &self,
        username: &str,
        session: CustomSession,
    ) -> Result<SessionResponse> {
        let url = format!("{URCHIN_BASE_URL}/player/sessions/custom");

        let mut query = vec![("player".to_string(), username.to_string())];

        match session {
            CustomSession::Duration(duration) => {
                query.push(("duration".to_string(), duration));
            }
            CustomSession::FromMs(from_ms) => {
                query.push(("from".to_string(), from_ms.to_string()));
            }
        }

        let res = self
            .client
            .get(url)
            .query(&query)
            .header("X-API-Key", &self.api_key)
            .send()
            .await?
            .error_for_status()?
            .json::<SessionResponse>()
            .await?;

        return Ok(res);
    }
}
