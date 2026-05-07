# GitHub Deployment Guide

This guide explains how to deploy the SCRIBE project to GitHub and set up GitHub Pages for the documentation site.

## Repository Setup

### 1. Create GitHub Repository
1. Go to https://github.com/AutoBotSolutions/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration
2. If the repository doesn't exist, create it with the name "SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration"
3. Set it as a public repository

### 2. Initialize Git Repository
```bash
cd /home/robbie/Desktop/scribe
git init
git add .
git commit -m "Initial commit - SCRIBE project with documentation"
```

### 3. Add Remote Repository
```bash
git remote add origin https://github.com/AutoBotSolutions/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration.git
```

### 4. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## GitHub Pages Setup

### 1. Enable GitHub Pages
1. Go to your repository on GitHub
2. Click on "Settings" tab
3. Scroll down to "Pages" section
4. Under "Build and deployment", select "GitHub Actions" as the source
5. Save the settings

### 2. Automatic Deployment
The GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) will automatically:
- Build the documentation site from the `scribe/site/` directory
- Deploy it to GitHub Pages
- Make it available at: `https://autobotsolutions.github.io/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration/`

### 3. Verify Deployment
After pushing to the main branch:
1. Go to the "Actions" tab in your repository
2. Wait for the "Deploy GitHub Pages" workflow to complete
3. Visit your GitHub Pages site to verify it's working

## Manual Deployment (Alternative)

If you prefer manual deployment instead of GitHub Actions:

### 1. Build Documentation Site
```bash
# The site is already built in scribe/site/
# No additional build steps needed
```

### 2. Use gh-pages Branch
```bash
# Install gh-pages if not already installed
npm install -g gh-pages

# Deploy to GitHub Pages
cd scribe/site
gh-pages -d . -b gh-pages
```

### 3. Configure GitHub Pages
1. Go to repository Settings > Pages
2. Select "Deploy from a branch"
3. Choose "gh-pages" branch and "/ (root)" folder
4. Save settings

## Project Structure

```
SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration/
├── README.md                 # Main project README
├── LICENSE                   # Commercial license
├── .gitignore               # Git ignore file
├── DEPLOYMENT.md            # This deployment guide
├── requirements.txt         # Python dependencies
├── config.json             # System configuration
├── main.py                 # Main application entry
├── start_api.sh            # API server starter
├── start_interactive.sh    # Interactive mode starter
├── validate_system.py      # System validation
├── test_system.py          # System tests
├── scribe/                 # Main source code
│   ├── src/                # Source modules
│   ├── site/               # Documentation site (GitHub Pages)
│   ├── docs/               # Source documentation
│   └── *.log               # Log files
└── .github/
    └── workflows/
        └── deploy-pages.yml # GitHub Actions workflow
```

## Troubleshooting

### GitHub Pages Not Working
1. Check the Actions tab for workflow errors
2. Ensure the repository is public (for free GitHub Pages)
3. Verify the `scribe/site/` directory exists and contains HTML files

### Git Push Issues
1. Ensure you have proper authentication set up
2. Use SSH instead of HTTPS if having issues:
   ```bash
   git remote set-url origin git@github.com:AutoBotSolutions/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration.git
   ```

### Documentation Links Broken
1. All links in the documentation are relative and should work on GitHub Pages
2. Localhost references are intentional for API documentation examples

## Post-Deployment

After successful deployment:

1. **Main Repository**: https://github.com/AutoBotSolutions/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration
2. **Documentation Site**: https://autobotsolutions.github.io/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration/
3. **API Documentation**: https://autobotsolutions.github.io/SCRIBE-Sonic-Resonance-Intelligence-and-Behavioral-Exploration/api.html

## Maintenance

- Update documentation by editing files in `scribe/site/`
- Commit and push changes to trigger automatic redeployment
- Monitor GitHub Actions for any deployment issues
- Regular updates should be made through pull requests for review

## Support

For deployment issues:
1. Check this guide first
2. Review GitHub Actions logs
3. Create an issue in the repository
4. Contact: autobotsolution@gmail.com
