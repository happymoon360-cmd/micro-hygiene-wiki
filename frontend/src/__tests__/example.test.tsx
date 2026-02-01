import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Simple test component for verification
function TestComponent() {
  return (
    <div>
      <h1 data-testid="title">Test Component</h1>
      <button>Click me</button>
      <p>Testing infrastructure is working!</p>
    </div>
  );
}

describe('Example Test Suite', () => {
  it('renders the test component correctly', () => {
    render(<TestComponent />);

    expect(screen.getByTestId('title')).toBeInTheDocument();
    expect(screen.getByText('Test Component')).toBeInTheDocument();
    expect(screen.getByText('Testing infrastructure is working!')).toBeInTheDocument();
  });

  it('renders button element', () => {
    render(<TestComponent />);

    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
  });

  it('handles user interactions', async () => {
    render(<TestComponent />);

    const button = screen.getByRole('button', { name: 'Click me' });
    await userEvent.click(button);

    // Verify button is clickable
    expect(button).toBeInTheDocument();
  });

  it('verifies custom jest-dom matchers', () => {
    render(<TestComponent />);

    const title = screen.getByTestId('title');

    // jest-dom custom matchers
    expect(title).toHaveTextContent('Test Component');
    expect(title).toBeVisible();
  });

  it('basic math test to verify test runner', () => {
    expect(2 + 2).toBe(4);
    expect(10 - 5).toBe(5);
  });
});
