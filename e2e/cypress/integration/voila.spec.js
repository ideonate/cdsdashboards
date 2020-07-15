
it('voila dashboard', () => {
  
  do_login()

  // Start My Server then back to Control Panel

  cy.get('#start')
    .should('contain', 'My Server').click()

  cy.get('#header-container > span:nth-child(4) > a', { timeout: 20000 })
    .should('contain', 'Control Panel').click()

  // Voila

  do_create_and_start_dashboard('Voila Test', 'Test.ipynb', 'voila')
  
  cy.get('#rendered_cells > main > div > div > div > div > div:nth-child(3) > div > div > div > div > pre')
    .should('contain', 'Voila top level is working')

  do_stop_dashserver('dash-voila-test')

  // Now try with git repo

  cy.visit('/hub/dashboards/voila-test/edit')

  cy.get('#tab-selector-gitrepo > a')
    .should('contain', 'Git Repo')
    .click()

  cy.get('#git_repo')
    .type('https://github.com/danlester/binder-sincos')

  cy.get('#dashboard-start-path')
    .clear()
    .type('Presentation.ipynb')

  cy.get('#source_type')
    .then( elem => { elem.val('gitrepo'); } )
    //.should('have.value', 'gitrepo')

  cy.get('#main > div > div > form > div > input[type=submit]')
    .click()

  cy.get('#launch')
    .should('contain', 'Go to Dashboard')
    .should('be.visible', { timeout: 20000 })
    .invoke('removeAttr', 'target').click() // Don't want to open in new tab

  cy.get('#Sin-and-Cos-Graph-demo')
    .should('contain', 'Sin and Cos Graph demo')

  do_stop_dashserver('dash-voila-test')

  // Plotly Dash

  do_create_and_start_dashboard('Plotly Dash Test', 'subfolder/subapp.py', 'plotlydash')
  
  cy.get('#react-entry-point > div > div:nth-child(2)')
    .should('contain', 'Dash: A web application framework for Python')

  cy.get('#react-entry-point > div > img')
  .should('be.visible')
  .and(($img) => {
    // "naturalWidth" and "naturalHeight" are set when the image loads
    expect($img[0].naturalWidth).to.be.greaterThan(0)
  })

  do_stop_dashserver('dash-plotly-dash-test')

  // Bokeh

  do_create_and_start_dashboard('Bokeh Test', 'bokeh/hello.py', 'bokeh')

  cy.get('input.bk-input').type('Dan')

  cy.get('button.bk-btn').click()

  cy.get('p.bk').should('contain', 'Hello, BokehDan')

  do_stop_dashserver('dash-bokeh-test')

})

