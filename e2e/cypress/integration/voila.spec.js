
it('voila dashboard', () => {
  
  do_login()

  cy.get('#start')
    .should('contain', 'My Server').click()

  cy.get('#header-container > span:nth-child(4) > a', { timeout: 20000 })
    .should('contain', 'Control Panel').click()

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(4) > a')
    .should('contain', 'Dashboards').click()

  cy.get('#start')
    .should('contain', 'New Dashboard').click()

  cy.get('#main > div > div > form > p:nth-child(2) > input[type=text]')
    .type('Voila Test')

  cy.get('#main > div > div > form > p:nth-child(12) > input[type=text]')
    .type('Test.ipynb')

  cy.get('#main > div > div > form > div > input[type=submit]')
    .click()

  cy.get('#launch')
    .should('contain', 'Go to Dashboard')
    .should('be.visible', { timeout: 20000 })
    .invoke('removeAttr', 'target').click() // Don't want to open in new tab

  // cy.get('#progress-message > a').click()
  
  cy.get('#rendered_cells > main > div > div > div > div > div:nth-child(3) > div > div > div > div > pre')
    .should('contain', 'test')

})

