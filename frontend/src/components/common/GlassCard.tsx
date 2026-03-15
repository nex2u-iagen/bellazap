import React from 'react';
import { Box, BoxProps } from '@chakra-ui/react';

export default function GlassCard({ children, ...props }: BoxProps) {
    return (
        <Box 
            bg="rgba(255, 255, 255, 0.7)" 
            backdropFilter="blur(10px)" 
            borderRadius="2xl" 
            p={6} 
            border="1px solid rgba(255, 255, 255, 0.3)" 
            shadow="xl" 
            {...props}
        >
            {children}
        </Box>
    );
}
