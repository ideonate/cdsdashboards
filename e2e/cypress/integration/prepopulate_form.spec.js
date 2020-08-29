it("should prepopulate the dashboard edition form", () => {
  do_login();

  cy.visit(
    "/hub/dashboards-new?name=My%20Dashboard&description=A%20populated%0Aform&start_path=%2Ftree%2Fpath%2Ffile.ipynb"
  );

  cy.get('#dashboard-name')
    .should('to.have.value', 'My Dashboard')

  cy.get('#dashboard-description')
    .should('to.have.text', 'A populated\nform')

  cy.get('#dashboard-start-path')
    .should('to.have.value', '/tree/path/file.ipynb')
});
