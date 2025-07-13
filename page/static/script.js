window.addEventListener('DOMContentLoaded', () => {
  fetch('/load-config')
    .then(res => res.json())
    .then(config => {
      applyConfig(config);
    })
    .catch(err => {
      console.error("Erreur lors du chargement de la config:", err);
    });
});



function switchSection(section) {
        // Update nav
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Only try to add active class if the nav item exists
        const navItem = document.querySelector(`[data-section="${section}"]`);
        if (navItem) {
            navItem.classList.add('active');
        }

        // Update content
        document.querySelectorAll('.content-section').forEach(sec => {
            sec.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        if (section === 'dashboard') {
            this.renderDashboard();
        }
    }

window.addEventListener("load", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const tab = urlParams.get("tab");
  if (tab === "config") {
    switchSection(tab);
  }
});

function applyConfig(config) {
  for (const category in config) {
    const tools = config[category];
    for (const tool in tools) {
      const settings = tools[tool];
      for (const key in settings) {
        const value = settings[key];

        if (key === "enabled") {
          // Case à cocher
          const checkboxId = `${tool}-${key}`;
          const checkbox = document.getElementById(checkboxId);
          if (checkbox) {
            checkbox.checked = Boolean(value);
          } else {
            console.warn(`Checkbox not found: ${checkboxId}`);
          }
        } else if (key === "apiKeys" && typeof value === "object") {
          // Champs API key
          for (const apiFieldId in value) {
            const input = document.getElementById(apiFieldId);
            if (input) {
              input.value = value[apiFieldId];
            }
          }
        }
      }
    }
  }
}

class ReconKitManager {
    constructor() {
        this.domains = [];
        this.currentDomain = null;
        this.toolsConfig = {
            subdomain: {
                subfinder: {
                    enabled: false
                },
                findomain: {
                    enabled: false
                },
                assetfinder: {
                    enabled: false
                },
                sublist3r: {
                    enabled: false
                },
                crtsh: {
                    enabled: false
                },
                chaos: {
                    enabled: false,
                    apiKeys: {
                        chaos: ''
                    }
                },
                
                securitytrails: {
                    enabled: false,
                    apiKeys: {
                        securitytrails: ''
                    }
                },
                virustotal: {
                    enabled: false,
                    apiKeys: {
                        virustotal: ''
                    }
                },
                alienvault: {
                    enabled: false,
                    apiKeys: {
                        alienvault: ''
                    }
                },
                dnsdumpster: {
                    enabled: false,
                    apiKeys: {
                        dnsdumpster: ''
                    }
                },
            },
            endpoint: {
                gau: {
                    enabled: false
                },
                waybackurls: {
                    enabled: false
                },
                waymore: {
                    enabled: false
                },
                katana: {
                    enabled: false
                },
                hakrawler: {
                    enabled: false
                },
                gospider: {
                    enabled: false
                },
                getJS: {
                    enabled: false
                },
                subjs: {
                    enabled: false
                },
            },
            screenshot: {
                aquatone: {
                    enabled: false
                },
                httpx: {
                    enabled: false
                }
            }
        };
        
        this.init();
    }

    init() {
        this.loadData();
        this.bindEvents();
        this.renderDashboard();
        this.updateStats();
        this.loadToolsConfig();
    }

    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchSection(item.dataset.section);
            });
        });

        // Configuration
        document.getElementById('saveConfigBtn').addEventListener('click', () => {
            this.saveToolsConfig();
        });

        document.getElementById('loadConfigBtn').addEventListener('click', () => {
            document.getElementById('configFileInput').click();
        });

        document.getElementById('configFileInput').addEventListener('change', (e) => {
            this.loadConfigFile(e.target.files[0]);
        });

        // Tool toggles
        document.querySelectorAll('.toggle-switch input').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                this.toggleTool(e.target);
            });
        });

        // Detail navigation
        document.getElementById('backToDashboard').addEventListener('click', () => {
            this.switchSection('dashboard');
        });

        // Detail tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchDetailTab(btn.dataset.tab);
            });
        });

        // Search and filters
        document.getElementById('endpointSearch')?.addEventListener('input', (e) => {
            this.filterEndpoints();
        });

        document.getElementById('statusFilter')?.addEventListener('change', () => {
            this.filterEndpoints();
        });

        document.getElementById('methodFilter')?.addEventListener('change', () => {
            this.filterEndpoints();
        });
    }

    switchSection(section) {
        // Update nav
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Only try to add active class if the nav item exists
        const navItem = document.querySelector(`[data-section="${section}"]`);
        if (navItem) {
            navItem.classList.add('active');
        }

        // Update content
        document.querySelectorAll('.content-section').forEach(sec => {
            sec.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        if (section === 'dashboard') {
            this.renderDashboard();
        }
    }

    renderDashboard() {
        const container = document.getElementById('domainsGrid');
        
        if (this.domains.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-globe"></i>
                    <h3>No domains analyzed yet</h3>
                    <p>Use your terminal to run reconnaissance scans on domains</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.domains.map(domain => `
            <div class="domain-card" onclick="reconKit.openDomainDetail('${domain.id}')">
                <div class="domain-card-header">
                    <div class="domain-name">${domain.name}</div>
                    <div class="domain-status status-${domain.status}">${domain.status}</div>
                </div>
                <div class="domain-description">${domain.description}</div>
                <div class="domain-meta">
                    <div class="scan-date">
                        <i class="fas fa-calendar"></i>
                        Scanned: ${new Date(domain.dateAdded).toLocaleDateString()}
                    </div>
                </div>
                <div class="domain-stats">
                    <div class="domain-stat">
                        <span class="domain-stat-number">${domain.subdomainsCount || 0}</span>
                        <span class="domain-stat-label">Subdomains</span>
                    </div>
                    <div class="domain-stat">
                        <span class="domain-stat-number">${domain.endpointsCount || 0}</span>
                        <span class="domain-stat-label">Endpoints</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    openDomainDetail(domainId) {
        this.currentDomain = this.domains.find(d => d.id == domainId);
        if (!this.currentDomain) return;

        document.getElementById('domainDetailTitle').textContent = this.currentDomain.name;
        this.switchSection('domain-detail');
        this.switchDetailTab('subdomains');
    }

    switchDetailTab(tab) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        // Update tab panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(tab).classList.add('active');

        // Load content based on tab
        switch(tab) {
            case 'subdomains':
                if (this.currentDomain && this.currentDomain.id) {
                    this.loadSubdomains(this.currentDomain.id);
                }
                break;
            case 'endpoints':
                this.loadEndpoints(this.currentDomain.id);
                break;
        }
    }




async loadSubdomains(domainId) {
    try {
        const res = await fetch(`/api/domain/${domainId}/subdomains`);
        if (!res.ok) throw new Error(`Erreur API: ${res.status}`);
        const subdomain = await res.json();

        if (!this.currentDomain) this.currentDomain = {};
        this.currentDomain.subdomain = subdomain;

        this.renderSubdomains();
    } catch (error) {
        console.error("Erreur lors du chargement des subdomains :", error);
        container.innerHTML = `<p>Impossible de charger les sous-domaines.</p>`;
    }
}

// Fonction qui ne fait que rendre les subdomains dans la page
renderSubdomains() {
    const container = document.getElementById('subdomainsContainer');

    if (!this.currentDomain || !this.currentDomain.subdomain || this.currentDomain.subdomain.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-sitemap"></i>
                <h3>No subdomains found</h3>
                <p>Run subdomain enumeration tools to discover subdomains</p>
            </div>
        `;
        return;
    }

    container.innerHTML = this.currentDomain.subdomain.map(subdomain => `
        <div class="subdomain-card" onclick="reconKit.openSubdomainDetailModal('${subdomain.name.replace(/'/g, "\\'")}')">
            <div class="subdomain-screenshot">
                <img src="${subdomain.screenshot || ''}" alt="${subdomain.name}" 
                     onerror="this.parentElement.innerHTML='<i class=\\'fas fa-image\\'></i><br>Screenshot not available'">
            </div>
            <div class="subdomain-info">
                <div class="subdomain-name">${subdomain.name}</div>
                <div class="subdomain-url"><a href="${subdomain.url}" target="_blank">${subdomain.url}</a></div>
               <div class="tech-stack">
  ${
    Array.isArray(subdomain.technologies) 
    ? subdomain.technologies.map(tech => {
        const httpStatus = tech.http_status || 'N/A';
        
        const target = tech.target || '';
        const plugins = tech.plugins || {};

        // Extraire quelques infos plugins utiles
        const ip = plugins.IP?.string?.[0] || '';
        const httpServer = plugins.HTTPServer?.string?.[0] || '';
        const country = plugins.Country?.string?.[0] || '';
        const title = plugins.Title?.string?.[0] || '';

        return `
          <div class="tech-summary">
            <span class="tech-tag">Status: ${httpStatus}</span>
            ${ip ? `<span class="tech-tag"> ${ip}</span>` : ''}
            ${httpServer ? `<span class="tech-tag">Server: ${httpServer}</span> `: ''}
          </div>
        `;
      }).join('')
    : ''
  }
</div>
            </div>
        </div>
    `).join('');
}



    openSubdomainDetailModal(subdomainName) {
        const modal = document.getElementById('subdomainDetail');
        const subdomain = this.currentDomain.subdomain.find(s => s.name === subdomainName);

        if (!subdomain) {
            console.error("Subdomain not found:", subdomainName);
            return;
        }

        // Construire le contenu détaillé de la modale
        let technologiesHtml = '';
        if (Array.isArray(subdomain.technologies) && subdomain.technologies.length > 0) {
            technologiesHtml = subdomain.technologies.map(tech => {
                const formattedTech = this.formatTechnology(tech); // Réutiliser la fonction existante
                return `<div class="detail-tech-item">${formattedTech}</div>`;
            }).join('');
        } else {
            technologiesHtml = '<p>No detailed technologies found.</p>';
        }

        modal.innerHTML = `
            <div class="modal-content">
                <button class="btn-close" onclick="reconKit.closeSubdomainDetailModal()">
                    <i class="fas fa-times"></i>
                </button>
                <h2>${subdomain.name}</h2>
                <div class="modal-body">
                    <div class="modal-screenshot">
                        <img src="${subdomain.screenshot || ''}" alt="${subdomain.name}" 
                             onerror="this.parentElement.innerHTML='<i class=\\'fas fa-image\\'></i><br>Screenshot not available'">
                    </div>
                    <div class="modal-info">
                        <p><strong>URL:</strong> <a href="${subdomain.url}" target="_blank">${subdomain.url}</a></p>
                        <p><strong>Status:</strong> <span class="status-${subdomain.status}">${subdomain.status}</span></p>
                        <h3>Technologies & Details:</h3>
                        <div class="tech-details-list">
                            ${technologiesHtml}
                        </div>
                    </div>
                </div>
            </div>
        `;
        modal.style.display = 'block';
        modal.classList.add('active'); // Pour les animations CSS
    }

    closeSubdomainDetailModal() {
        const modal = document.getElementById('subdomainDetail');
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300); // Correspond à la durée de l'animation CSS
    }





 formatTechnology(tech) {
  const httpStatus = tech.http_status || 'N/A';
  const plugins = tech.plugins || {};
  const target = tech.target || '';
  

  // Extraits simples
  const ip = plugins.IP?.string?.[0] || '';
  const httpServer = plugins.HTTPServer?.string?.[0] || '';
  const title = plugins.Title?.string?.[0] || '';
  const wordpressVersion = plugins.WordPress?.version?.[0] || '';
  const jqueryVersion = plugins.JQuery?.version?.[0] || '';
  const country = plugins.Country?.module?.[0] || '';

  let info = [];

  if (httpStatus) info.push(`Status: ${httpStatus}`);
  if (httpServer) info.push(`Server: ${httpServer}`);
  if (title) info.push(`Title: ${title}`);
  if (wordpressVersion) info.push(`WordPress v${wordpressVersion}`);
  if (jqueryVersion) info.push(`jQuery v${jqueryVersion}`);
  if (country) info.push(`Country: ${country}`);

  return info.join(' | ');
}




async loadEndpoints(domainId) {
  try {
    const res = await fetch(`/api/domain/${domainId}/endpoints`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const data = await res.json();

    this.currentDomain.endpoint = data.map(item => ({
      method: item.method || 'GET',
      url: item.url,
      status: item.status_code || item.status || 'N/A'
    }));

    this.renderEndpoints();
  } catch (e) {
    console.error('Failed to load endpoints:', e);
  }
}






    renderEndpoints() {
        const container = document.getElementById('endpointsContainer');
        
        if (!this.currentDomain || this.currentDomain.endpoint.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-route"></i>
                    <h3>No endpoints found</h3>
                    <p>Run endpoint discovery tools to find URLs and parameters</p>
                </div>
            `;
            return;
        }

        this.renderEndpointsList(this.currentDomain.endpoint);
    }



    renderEndpointsList(endpoints) {
        const container = document.getElementById('endpointsContainer');
        
        container.innerHTML = endpoints.map(endpoint => `
            <div class="endpoint-item">
                <span class="endpoint-method method-${endpoint.method.toLowerCase()}">${endpoint.method}</span>
                <span class="endpoint-url">${endpoint.url}</span>
                <span class="endpoint-status status-${endpoint.status}">${endpoint.status}</span>
            </div>
        `).join('');
    }




    filterEndpoints() {
        if (!this.currentDomain) return;

        const searchTerm = document.getElementById('endpointSearch').value.toLowerCase();
        const statusFilter = document.getElementById('statusFilter').value;
        const methodFilter = document.getElementById('methodFilter').value;

        let filtered = this.currentDomain.endpoint.filter(endpoint => {
            const matchesSearch = endpoint.url.toLowerCase().includes(searchTerm);
            const matchesStatus = !statusFilter || endpoint.status.toString() === statusFilter;
            const matchesMethod = !methodFilter || endpoint.method === methodFilter;
            
            return matchesSearch && matchesStatus && matchesMethod;
        });

        this.renderEndpointsList(filtered);
    }





    toggleTool(toggle) {
        const toolCard = toggle.closest('.tool-card');
        const toolName = toolCard.dataset.tool;
        
        if (toggle.checked) {
            toolCard.classList.add('enabled');
        } else {
            toolCard.classList.remove('enabled');
        }
        
        // Update config
        this.updateToolConfig(toolName, toggle.checked);
    }



    updateToolConfig(toolName, enabled) {
        // Find the tool in config and update
        for (const category in this.toolsConfig) {
            if (this.toolsConfig[category][toolName]) {
                this.toolsConfig[category][toolName].enabled = enabled;
                break;
            }
        }
    }











saveToolsConfig() {

    fetch('/save-config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.toolsConfig)
    })
    .then(res => {
        if (!res.ok) throw new Error("Erreur réseau");
        return res.text();
    })
    .then(msg => {
        this.showNotification(msg, 'success');
    })
    .catch(err => {
        this.showNotification("Erreur lors de l'enregistrement", 'error');
        console.error(err);
    });
}







loadToolsConfig() {
    fetch('/load-config')
        .then(res => res.json())
        .then(config => {
            this.toolsConfig = { ...this.toolsConfig, ...config };
            this.applyConfigToUI();
        })
        .catch(err => {
            console.error('Erreur de chargement de la config :', err);
        });
}





    updateStats() {
        const totalDomains = this.domains.length;
        const totalSubdomains = this.domains.reduce((sum, domain) => sum + (domain.subdomainsCount || 0), 0);
        const totalEndpoints = this.domains.reduce((sum, domain) => sum + (domain.endpointsCount || 0), 0);

        
        document.getElementById('totalDomains').textContent = totalDomains;
        document.getElementById('totalSubdomains').textContent = totalSubdomains;
        document.getElementById('totalEndpoints').textContent = totalEndpoints;
    }






    async loadData() {
    try {
        const res = await fetch('/api/domains');
        const domainSummaries = await res.json();

        const domainPromises = domainSummaries.map(async (summary) => {
            const detailRes = await fetch(`/api/domain/${summary.id}`);
            const detail = await detailRes.json();
            console.log('Raw data:', detail.subdomains, detail.endpoints, typeof detail.subdomains, typeof detail.endpoints);
            return {
                ...detail,
                subdomains: detail.subdomains || [],
                endpoints: detail.endpoints || [],
                subdomainsCount: typeof detail.subdomains === 'number' ? detail.subdomains : (detail.subdomains || []).length,
                endpointsCount: typeof detail.endpoints === 'number' ? detail.endpoints : (detail.endpoints || []).length
            };
        });

        this.domains = await Promise.all(domainPromises);

        this.updateStats();
        this.renderDashboard();
    } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
        this.domains = [];
        this.renderDashboard();
    }
}

    saveData() {
        localStorage.setItem('reconkit_domains', JSON.stringify(this.domains));
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check' : type === 'error' ? 'fa-times' : 'fa-info'}"></i>
            ${message}
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove notification
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the application
const reconKit = new ReconKitManager();