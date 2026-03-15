import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

const config: ThemeConfig = {
    initialColorMode: 'light',
    useSystemColorMode: false,
}

const theme = extendTheme({
    config,
    colors: {
        brand: {
            50: '#f9f5f0',
            100: '#efdfcc',
            200: '#e5caaa',
            300: '#dbb487',
            400: '#d19f65',
            500: '#C5A059', // Champagne Gold
            600: '#a38349',
            700: '#81663a',
            800: '#5e4a2a',
            900: '#3c2f1b',
        },
        dark: {
            900: '#1A1A1A', // Velvet Black
            800: '#2D2D2D',
        }
    },
    fonts: {
        heading: "'Playfair Display', serif",
        body: "'Inter', sans-serif",
    },
    components: {
        Button: {
            baseStyle: {
                borderRadius: 'full',
                fontWeight: '500',
                textTransform: 'uppercase',
                letterSpacing: '1px',
            },
            variants: {
                solid: (props: any) => ({
                    bg: props.colorScheme === 'brand' ? 'brand.500' : undefined,
                    color: 'white',
                    _hover: {
                        bg: 'brand.600',
                        transform: 'translateY(-2px)',
                        boxShadow: 'lg',
                    },
                    transition: 'all 0.3s ease',
                }),
                outline: {
                    border: '2px solid',
                    borderColor: 'brand.500',
                    color: 'brand.500',
                    _hover: {
                        bg: 'brand.50',
                    }
                }
            }
        },
        Card: {
            baseStyle: {
                container: {
                    borderRadius: '2xl',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.05)',
                    border: '1px solid',
                    borderColor: 'gray.100',
                    bg: 'white',
                }
            }
        }
    }
})

export default theme
