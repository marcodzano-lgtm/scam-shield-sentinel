const axios = require('axios');

const NEYNAR_API_KEY = process.env.NEYNAR_API_KEY;

async function searchCasts() {
    try {
        const response = await axios.get('https://api.neynar.com/v2/farcaster/cast/search', {
            params: {
                q: 'OpenClaw',
                limit: 10
            },
            headers: {
                'api_key': NEYNAR_API_KEY
            }
        });
        
        const casts = response.data.result.casts;
        const threats = casts.filter(c => 
            c.text.toLowerCase().includes('scam') || 
            c.text.toLowerCase().includes('malicious') || 
            c.text.toLowerCase().includes('exploit') ||
            c.text.toLowerCase().includes('threat')
        );
        
        console.log(JSON.stringify(threats, null, 2));
    } catch (error) {
        console.error(JSON.stringify(error.response?.data || error.message, null, 2));
    }
}

searchCasts();
