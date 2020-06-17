
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

  // Bokeh

  do_create_and_start_dashboard('Bokeh Test', 'bokeh/hello.py', 'bokeh')

  cy.get('input.bk-input').type('Dan')

  cy.get('button.bk-btn').click()

  cy.get('p.bk').should('contain', 'Hello, BokehDan')


})

