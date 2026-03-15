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
} from '@chakra-ui/react'
import { MessageCircle, ShieldCheck, ArrowRight } from 'lucide-react'

export default function Login({ onLogin }: { onLogin: () => void }) {
    const [step, setStep] = useState(1) // 1: Identificação, 2: Token
    const [identifier, setIdentifier] = useState('')
    const [token, setToken] = useState('')
    const [loading, setLoading] = useState(false)
    const toast = useToast()

    const handleSendToken = async () => {
        if (!identifier) {
            toast({
                title: "Campo obrigatório",
                description: "Por favor, insira seu WhatsApp ou CPF.",
                status: "warning",
            })
            return
        }
        setLoading(true)
        // Simula envio de token via backend -> WhatsApp
        setTimeout(() => {
            setLoading(false)
            setStep(2)
            toast({
                title: "Token enviado!",
                description: "Enviamos seu código de acesso para o seu WhatsApp cadastrado.",
                status: "success",
            })
        }, 1500)
    }

    const handleVerifyToken = async () => {
        if (token.length < 4) return
        setLoading(true)
        // Simula verificação
        setTimeout(() => {
            setLoading(false)
            onLogin()
        }, 1200)
    }

    return (
        <Flex minH="100vh" align="center" justify="center" bg="brand.50" px={4}>
            <ScaleFade initialScale={0.9} in={true}>
                <Box
                    bg="white"
                    p={10}
                    w={{ base: "full", md: "450px" }}
                    borderRadius="3xl"
                    boxShadow="2xl"
                    position="relative"
                    overflow="hidden"
                >
                    {/* Decorative element */}
                    <Box
                        position="absolute"
                        top="-50px"
                        right="-50px"
                        w="150px"
                        h="150px"
                        bg="brand.100"
                        borderRadius="full"
                        opacity={0.5}
                        zIndex={0}
                    />

                    <VStack spacing={8} position="relative" zIndex={1}>
                        <Heading size="lg" color="dark.900" letterSpacing="tight" textAlign="center">
                            BellaZap <Text as="span" color="brand.500">✨</Text>
                        </Heading>

                        {step === 1 ? (
                            <VStack spacing={6} w="full">
                                <Box textAlign="center">
                                    <Heading size="md" mb={2}>Bem-vinda de volta</Heading>
                                    <Text color="gray.500">Acesse sua conta de forma segura e rápida</Text>
                                </Box>

                                <Stack w="full" spacing={4}>
                                    <Box>
                                        <Text mb={2} fontSize="sm" fontWeight="bold" color="gray.600">WhatsApp ou CPF</Text>
                                        <Input
                                            placeholder="Ex: 11999999999"
                                            size="lg"
                                            variant="filled"
                                            bg="gray.100"
                                            _focus={{ bg: 'white', borderColor: 'brand.500' }}
                                            value={identifier}
                                            onChange={(e) => setIdentifier(e.target.value)}
                                        />
                                    </Box>
                                    <Button
                                        colorScheme="brand"
                                        size="lg"
                                        w="full"
                                        rightIcon={<ArrowRight size={20} />}
                                        isLoading={loading}
                                        onClick={handleSendToken}
                                    >
                                        Receber Acesso
                                    </Button>
                                </Stack>
                                <Text fontSize="xs" color="gray.400" textAlign="center">
                                    Ao continuar, você concorda com nossos Termos de Uso e Privacidade.
                                </Text>
                            </VStack>
                        ) : (
                            <VStack spacing={6} w="full">
                                <Center w="60px" h="60px" bg="brand.50" borderRadius="2xl" color="brand.500">
                                    <ShieldCheck size={32} />
                                </Center>
                                <Box textAlign="center">
                                    <Heading size="md" mb={2}>Verifique seu WhatsApp</Heading>
                                    <Text color="gray.500">Insira o código de 4 dígitos enviado para você.</Text>
                                </Box>

                                <Stack w="full" spacing={4}>
                                    <Input
                                        placeholder="0000"
                                        size="lg"
                                        textAlign="center"
                                        fontSize="2xl"
                                        letterSpacing="10px"
                                        fontWeight="bold"
                                        maxLength={4}
                                        variant="filled"
                                        bg="gray.100"
                                        _focus={{ bg: 'white', borderColor: 'brand.500' }}
                                        value={token}
                                        onChange={(e) => setToken(e.target.value)}
                                    />
                                    <Button
                                        colorScheme="brand"
                                        size="lg"
                                        w="full"
                                        isLoading={loading}
                                        onClick={handleVerifyToken}
                                    >
                                        Confirmar e Entrar
                                    </Button>
                                    <Button variant="ghost" size="sm" onClick={() => setStep(1)}>
                                        Alterar número
                                    </Button>
                                </Stack>
                            </VStack>
                        )}
                    </VStack>
                </Box>
            </ScaleFade>
        </Flex>
    )
}
