// captureHomeDepot.js

// Triggered from popup.html

document.getElementById('saveBtn').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
    // Inject turndown.js into the page first
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['turndown.js']
    }, () => {
      // Then inject the scraping function
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: scrapeAndSaveArticle
      }, () => window.close());
    });
  });
  
  async function scrapeAndSaveArticle() {
    if (typeof TurndownService === 'undefined') {
      alert('❌ Turndown.js library not found.');
      return;
    }
  
    const kebabCase = (str) =>
      str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  
    try {
      const title = document.querySelector('h1')?.innerText || document.title;
      const kebabTitle = kebabCase(title);
  
      const publishMatch = document.body.innerText.match(/(?:Published|Last updated)\s+(\w+ \d{1,2}, \d{4})/i);
      const publishDate = publishMatch ? publishMatch[1] : 'Unknown';
  
      const mainContent = document.querySelector('#main-content') || document.querySelector('article');
      if (!mainContent) throw new Error('Main content not found.');
  
      // Clean junk elements
      const junkSelectors = [
        'nav',
        '#header-static',
        '#footer-static',
        '.site-map',
        '.breadcrumb',
        '.sf-header',
        '.sf-footer',
        '.sf-mobile-footer'
      ];
      junkSelectors.forEach(sel =>
        mainContent.querySelectorAll(sel).forEach(el => el.remove())
      );
  
      const turndownService = new TurndownService({ headingStyle: 'atx' });
      turndownService.keep(['img', 'a']);
  
      const firstImg = document.querySelector('img')?.src || '';
      const mdHeader = `# ${title}\n\n![thumbnail](${firstImg})\n\nPublished ${publishDate}\n\n`;
      const markdownBody = turndownService.turndown(mainContent.innerHTML);
  
      const finalMarkdown = `${mdHeader}${markdownBody}\n\n[Read Original](${location.href})`;
  
      const blob = new Blob([finalMarkdown], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
  
      const a = document.createElement('a');
      a.href = url;
      a.download = `${kebabTitle}.md`;
      a.click();
  
      URL.revokeObjectURL(url);
    } catch (e) {
      alert('❌ Failed to scrape this page.');
      console.error(e);
    }
  }
  