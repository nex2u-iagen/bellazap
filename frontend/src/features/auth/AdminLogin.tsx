import React, { useState } from 'react'
import {
    Box,
    Flex,
    Stack,
    Heading,
    Text,
    Input,
    Button,
    VStack,
    useToast,
    Link,
    ScaleFade,
    Center,
    Icon,
    FormControl,
    FormLabel,
} from '@chakra-ui/react'
import { Lock, ArrowRight, ShieldAlert } from 'lucide-react'

export default function AdminLogin({ onLogin }: { onLogin: () => void }) {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const toast = useToast()

    const handleAdminLogin = async () => {
        if (!email || !password) {
            toast({
                title: "Dados incompletos",
                description: "Preencha e-mail e senha de administrador.",
                status: "warning",
            })
            return
        }
        setLoading(true)

        // Simula verificação de Super Admin
        setTimeout(() => {
            setLoading(false)
            if (email === 'admin@bellazap.com' && password === 'admin123') { // Mock segurança
                onLogin()
                toast({
                    title: "Acesso Admin",
                    description: "Bem-vindo ao centro de comando BellaZap.",
                    status: "success",
                })
            } else {
                toast({
                    title: "Erro de acesso",
                    description: "Credenciais de administrador inválidas.",
                    status: "error",
                })
            }
        }, 1500)
    }

    return (
        <Flex minH="100vh" align="center" justify="center" bg="dark.900" px={4}>
            <ScaleFade initialScale={0.9} in={true}>
                <Box
                    bg="white"
                    p={10}
                    w={{ base: "full", md: "400px" }}
                    borderRadius="2xl"
                    boxShadow="dark-lg"
                >
                    <VStack spacing={8}>
                        <VStack spacing={2} textAlign="center">
                            <Center w="50px" h="50px" bg="red.50" borderRadius="full" color="red.500">
                                <ShieldAlert size={28} />
                            </Center>
                            <Heading size="md" color="dark.900">Área do Administrador</Heading>
                            <Text fontSize="sm" color="gray.500">Acesso restrito para gestão da plataforma.</Text>
                        </VStack>

                        <Stack w="full" spacing={4}>
                            <FormControl>
                                <FormLabel fontSize="xs" fontWeight="bold">E-MAIL ADMIN</FormLabel>
                                <Input
                                    type="email"
                                    placeholder="admin@bellazap.com"
                                    variant="filled"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel fontSize="xs" fontWeight="bold">SENHA</FormLabel>
                                <Input
                                    type="password"
                                    placeholder="******"
                                    variant="filled"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </FormControl>
                            <Button
                                colorScheme="red"
                                size="lg"
                                w="full"
                                leftIcon={<Lock size={18} />}
                                isLoading={loading}
                                onClick={handleAdminLogin}
                            >
                                Autenticar Admin
                            </Button>
                        </Stack>

                        <Link href="/" fontSize="sm" color="gray.400">Voltar para área do usuário</Link>
                    </VStack>
                </Box>
            </ScaleFade>
        </Flex>
    )
}
