/**
 * Touch-friendly score button component
 * Minimum 44x44px as per NFR requirements
 */
import { Button, ButtonProps } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledButton = styled(Button)(({ theme }) => ({
  minWidth: '56px',
  minHeight: '56px',
  fontSize: '1.25rem',
  fontWeight: 600,
  borderRadius: theme.spacing(1),
  touchAction: 'manipulation', // Improve touch responsiveness
  userSelect: 'none',
  WebkitTapHighlightColor: 'transparent',
  '&:active': {
    transform: 'scale(0.95)',
  },
  transition: 'transform 0.1s ease-in-out',
}));

interface ScoreButtonProps extends ButtonProps {
  score?: number;
  isSelected?: boolean;
}

export const ScoreButton: React.FC<ScoreButtonProps> = ({
  score,
  isSelected = false,
  children,
  ...props
}) => {
  return (
    <StyledButton
      variant={isSelected ? 'contained' : 'outlined'}
      color={isSelected ? 'primary' : 'inherit'}
      {...props}
    >
      {children || score}
    </StyledButton>
  );
};
