import { test, expect } from '@playwright/test';

test.describe(`PI Quest`, () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the home page before each test
    await page.goto('http://localhost:3000');
  });

  test(`should show sun and sun info`, async({ page }) => {
    await expect(page.getByText(`Sun Information`)).toBeVisible()

    const sunVisualizer = page.getByTestId(`sun-visualizer`)
    await expect(sunVisualizer).toBeVisible()
  })


  test(`should able to convert km to miles when uom toggled`, async ({ page }) => {
    // Locate the unit toggle switch
    const switchToggle = page.getByTestId('unit-toggle');
    await expect(switchToggle).toHaveAttribute('aria-checked', 'false'); // Initially set to km
  
    // Verify initial values in km
    const circumferenceElem = page.getByTestId('circumference');
    await expect(circumferenceElem).toBeVisible();
    await expect(circumferenceElem).toHaveText(/km/);
  
    const radiusElem = page.getByTestId('radius');
    await expect(radiusElem).toBeVisible();
    await expect(radiusElem).toHaveText(/km/);
  
    const distanceFromEarthElem = page.getByTestId('distance-from-earth');
    await expect(distanceFromEarthElem).toBeVisible();
    await expect(distanceFromEarthElem).toHaveText(/km/);
  
    // Toggle the switch to miles
    await switchToggle.click();
    await expect(switchToggle).toHaveAttribute('aria-checked', 'true'); // Now set to miles
  
    // Verify updated values in miles
    await expect(circumferenceElem).toHaveText(/miles/);
    await expect(radiusElem).toHaveText(/miles/);
    await expect(distanceFromEarthElem).toHaveText(/miles/);
  });


  test(`should show pop up dialog when the pi help icon clicked`, async({ page }) => {
    // Click the help icon
    const helpIcon = page.getByTestId('info-icon'); 
    await helpIcon.click();

    // Check if the dialog is visible
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    // We don't verify the content for now as we don't have backend

    // Close the dialog
    const closeButton = dialog.getByRole('button', { name: /close/i }); 
    await closeButton.click();

    // Check if the dialog is closed
    await expect(dialog).not.toBeVisible();
  })
})
