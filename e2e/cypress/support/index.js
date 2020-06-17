
do_login = () => {
  
  cy.visit('/hub/home')

  cy.get('#username_input')
    .type('dan')

    cy.get('#password_input')
    .type('password')

  cy.get('form').submit()

}

do_create_and_start_dashboard = (name, path, framework) => {

  cy.visit('/hub/home')

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(4) > a')
    .should('contain', 'Dashboards').click()

  cy.get('#start')
    .should('contain', 'New Dashboard').click()

  cy.get('#main > div > div > form > p:nth-child(2) > input[type=text]')
    .type(name)

  cy.get('#main > div > div > form > p:nth-child(12) > input[type=text]')
    .type(path)

  cy.get('#presentation_type')
    .select(framework)

  cy.get('#main > div > div > form > div > input[type=submit]')
    .click()

  cy.get('#launch')
    .should('contain', 'Go to Dashboard')
    .should('be.visible', { timeout: 20000 })
    .invoke('removeAttr', 'target').click() // Don't want to open in new tab

}

do_stop_dashserver = (id) => {
  cy.visit('/hub/home')

  cy.get('#stop-'+id)
    .should('contain', 'stop').click()

  cy.get('#start-'+id)
    .should('be.visible', { timeout: 20000 })
    .should('contain', 'start') // Appears when stop complete

}
