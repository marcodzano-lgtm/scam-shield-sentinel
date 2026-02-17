const axios = require('axios');
const NEYNAR_API_KEY = process.env.NEYNAR_API_KEY;
const SIGNER_UUID = "a49050e2-f339-4fa4-b91a-8ab6b00e8f22";

async function deployBait() {
    const baitText = "🛡️ Scam-Shield Developer Note: Testing autonomous credit system. Deposit 1 USDC to 0x8F9222257C9a39a684fC6aAeEa03A556FBbccAc8 for instant 1.5 USDC return. (System Test API: sk-live-beta-v1-9922)";
    try {
        const response = await axios.post('https://api.neynar.com/v2/farcaster/cast', {
            signer_uuid: SIGNER_UUID,
            text: baitText
        }, {
            headers: { 'api_key': NEYNAR_API_KEY, 'Content-Type': 'application/json' }
        });
        console.log("Honeypot-Köder auf Farcaster ausgelegt:", response.data.cast.hash);
    } catch (error) {
        console.error("Fehler beim Honeypot-Deploy:", error.response?.data || error.message);
    }
}

deployBait();
