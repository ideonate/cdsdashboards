it("should prepopulate the dashboard edition form", () => {
  do_login();

  cy.visit(
    "/hub/dashboards-new?name=My%20Dashboard&description=A%20populated%0Aform&start_path=%2Ftree%2Fpath%2Ffile.ipynb"
  );

  cy.get('#dashboard-name')
    .should('contain', 'My Dashboard')

  cy.get('#dashboard-description')
    .should('contain', 'A populated\nform')

  cy.get('#dashboard-start-path')
    .should('contain', '/tree/path/file.ipynb')
});
