# API Setup Guide

This guide explains how to get and configure API keys for data acquisition.

## Getting API Keys

### NOAA Climate Data Online Token

1. Go to https://www.ncdc.noaa.gov/cdo-web/token
2. Enter your email address
3. Click "Request Token"
4. Check your email (should arrive within a few minutes to hours)
5. Save the token

Example token format: `AbCdEfGhIjKlMnOpQrStUvWxYz123456`

### USDA NASS QuickStats API Key

1. Go to https://quickstats.nass.usda.gov/api
2. Fill out the request form with your email
3. Click "Request API Key"
4. Check your email (should arrive immediately)
5. Save the key

Example key format: `12345678-ABCD-1234-ABCD-123456789ABC`

## Configuring Your Keys

### Method 1: Interactive Setup (Recommended)

Run the setup script and paste your keys when prompted:

```bash
python setup_api_keys.py
```

The script will update `config.py` automatically.

### Method 2: Manual Configuration

Open `config.py` in a text editor and find these lines:

```python
NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', 'YOUR_NOAA_TOKEN_HERE')
USDA_API_KEY = os.getenv('USDA_API_KEY', 'YOUR_USDA_KEY_HERE')
```

Replace the placeholder values with your actual keys:

```python
NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', 'AbCdEfGhIjKlMnOpQrStUvWxYz123456')
USDA_API_KEY = os.getenv('USDA_API_KEY', '12345678-ABCD-1234-ABCD-123456789ABC')
```

Save the file.

### Method 3: Environment Variables

For better security, you can set environment variables instead of editing files:

```bash
export NOAA_API_TOKEN='your_token_here'
export USDA_API_KEY='your_key_here'
```

To make these permanent, add them to your `~/.bashrc` or `~/.zshrc` file.

## Verifying Configuration

Check if your keys are configured correctly:

```bash
python config.py
```

You should see:
```
NOAA API Token: Set
USDA API Key:   Set
```

If you see "Not set", the configuration didn't work.

## Using the API Keys

Once configured, the data acquisition scripts will automatically use your keys:

```bash
python scripts/get_noaa_data.py   # Uses NOAA token
python scripts/get_usda_data.py   # Uses USDA key
```

## Troubleshooting

### "API token not set" error

Check that you:
- Edited the correct `config.py` file (should be in project root)
- Copied the key exactly (no extra spaces or line breaks)
- Saved the file after editing

Try running `python config.py` to verify.

### "HTTP 401 Unauthorized" error

Your API key is invalid or expired. Possible causes:
- Typo when copying the key
- Using the wrong key for the wrong API
- Key expired (request a new one)

### "HTTP 429 Rate Limit" error

You've made too many requests. The scripts have built-in delays to prevent this, but if you run them repeatedly in a short time, you may hit limits. Wait a few minutes and try again.

### NOAA download is very slow

This is normal. NOAA has millions of daily weather records. For 1990-2023, expect 10-30 minutes of download time.

To speed up testing, reduce the date range in `config.py`:
```python
DATA_START_YEAR = 2015  # Instead of 1990
DATA_END_YEAR = 2023
```

## Security Best Practices

- Don't commit `config.py` to Git if it contains real API keys
- Consider using environment variables for production
- Don't share your API keys publicly
- Request new keys if you think they've been compromised

## API Rate Limits

Both APIs have rate limits:
- **NOAA:** 1000 requests per day per token
- **USDA:** No published limit, but be respectful

Our scripts include delays between requests to avoid hitting limits. The NOAA script uses 0.2 second delays, and the USDA script uses 1 second delays.

## Testing Without Full Data

If you want to test the pipeline before downloading full datasets, you can create small sample files. See the "Sample Data" section in the main README.

## Getting Help

- **NOAA API Documentation:** https://www.ncdc.noaa.gov/cdo-web/webservices/v2
- **USDA API Documentation:** https://quickstats.nass.usda.gov/api
- **NOAA Support:** ncei.orders@noaa.gov
- **USDA Support:** nass@usda.gov

## Next Steps

After configuring your keys:

1. Verify configuration: `python config.py`
2. Download NOAA data: `python scripts/get_noaa_data.py`
3. Download USDA data: `python scripts/get_usda_data.py`
4. Run the pipeline: `./workflow/run_all.sh`
