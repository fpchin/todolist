/**
 * Error alert component
 */
import { Alert, AlertTitle, Box } from '@mui/material';

interface ErrorAlertProps {
  error: string;
  onClose?: () => void;
  title?: string;
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({
  error,
  onClose,
  title = 'Error',
}) => {
  return (
    <Box mb={2}>
      <Alert severity="error" onClose={onClose}>
        <AlertTitle>{title}</AlertTitle>
        {error}
      </Alert>
    </Box>
  );
};
