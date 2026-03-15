import React, { useState, useEffect, useRef } from 'react'
import { Routes, Route, useNavigate, useLocation, Link } from 'react-router-dom'
import {
    Box, Flex, Heading, Button, Stack, Text, Container, Grid, GridItem,
    Icon, Avatar, Menu, MenuButton, MenuList, MenuItem, Stat, StatLabel,
    StatNumber, StatHelpText, Badge, useToast, Table, Thead, Tbody, Tr, Th,
    Td, TableContainer, FormControl, FormLabel, Input, Select, Modal,
    ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody,
    ModalCloseButton, useDisclosure, Divider, HStack, Progress,
    IconButton, Textarea, Switch, Tabs, TabList, TabPanels, Tab, TabPanel,
    VStack, SimpleGrid, NumberInput, NumberInputField, Alert, AlertIcon,
    Skeleton, Accordion, AccordionItem, AccordionButton, AccordionPanel,
    AccordionIcon, Center
} from '@chakra-ui/react'
import {
    LayoutDashboard, ShoppingBag, Wallet, LogOut, ChevronRight, Bell,
    Sparkles, Settings, Users, ArrowUpRight, Plus, Eye, Cpu, TrendingUp,
    CreditCard, MessageSquare, Activity, ShieldCheck, Server, Database,
    RefreshCcw, Upload, Zap, Lock, HardDrive, Bot, Trash2, HelpCircle,
    FileText, Info
} from 'lucide-react'
import axios from 'axios'
import Login from './features/auth/Login'
import AdminLogin from './features/auth/AdminLogin'

import AdminRevendedoras from './features/admin/AdminRevendedoras'
import AdminLLMManager from './features/admin/AdminLLMManager'
import AdminDBExplorer from './features/admin/AdminDBExplorer'
import AdminSettings from './features/admin/AdminSettings'
import AdminAnalytics from './features/admin/AdminAnalytics'
import AdminAgents from './features/admin/AdminAgents'
import GlassCard from './components/common/GlassCard'

const API_BASE = "http://localhost:8000/api/v1"

// --- Product Upload Component (Kept as local for now or can be moved) ---
function ProductUpload() {
    const [loading, setLoading] = useState(false)
    const fileInputRef = useRef<HTMLInputElement>(null)
    const toast = useToast()

    const handleUpload = async (e: any) => {
        const file = e.target.files[0]
        if (!file) return
        setLoading(true)
        const formData = new FormData()
        formData.append('file', file)
        try {
            const res = await axios.post(`${API_BASE}/admin/produtos/import`, formData)
            toast({ title: res.data.message, status: 'success' })
        } catch (e) {
            toast({ title: 'Erro no upload', status: 'error' })
        } finally {
            setLoading(false)
        }
    }

    return (
        <GlassCard>
            <Heading size="md" mb={4}>Atualizar Base de Produtos</Heading>
            <Text color="gray.600" fontSize="sm" mb={4}>
                Use esta ferramenta para enviar uma nova lista de produtos para a plataforma (.CSV).
            </Text>
            <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={handleUpload} accept=".csv" />
            <Button leftIcon={<Upload size={18} />} variant="outline" colorScheme="pink" isLoading={loading} onClick={() => fileInputRef.current?.click()}>
                Importar Planilha (.CSV)
            </Button>
        </GlassCard>
    )
}

// --- Views ---

function Dashboard() {
    return (
        <Container maxW="container.xl" py={8}>
            <Stack spacing={8}>
                <Flex justify="space-between" align="center">
                    <Box><Heading size="lg" fontWeight="700" fontFamily="Playfair Display">Olá, Estrela ✨</Heading><Text color="gray.500">Acompanhe seu progresso de vendas.</Text></Box>
                    <HStack spacing={4}>
                        <Button leftIcon={<Bell size={18} />} variant="ghost" borderRadius="full">Notificações</Button>
                        <Badge colorScheme="green" variant="subtle" px={3} py={1} borderRadius="full">Online</Badge>
                    </HStack>
                </Flex>
                <Grid templateColumns={{ base: "repeat(1, 1fr)", md: "repeat(3, 1fr)" }} gap={6}>
                    <GridItem><GlassCard><Stat><StatLabel color="gray.500" textTransform="uppercase" fontSize="xs">Saldo Disponível</StatLabel><StatNumber fontSize="3xl" color="pink.500">R$ 1.250,00</StatNumber><StatHelpText>Split ativo (8%)</StatHelpText></Stat></GlassCard></GridItem>
                    <GridItem><GlassCard><Stat><StatLabel color="gray.500" textTransform="uppercase" fontSize="xs">Vendas do Mês</StatLabel><StatNumber fontSize="3xl">32 / 100</StatNumber><StatHelpText>Plano Bella Pro</StatHelpText></Stat></GlassCard></GridItem>
                    <GridItem><Box p={6} bg="orange.400" color="white" borderRadius="2xl" shadow="xl"><Stat><StatLabel opacity={0.8} textTransform="uppercase" fontSize="xs">Lançamento</StatLabel><StatNumber fontSize="2xl">Natura Una Gold</StatNumber><StatHelpText opacity={0.8}>Disponível 24/02</StatHelpText></Stat></Box></GridItem>
                </Grid>
                
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
                    <GlassCard>
                        <Heading size="md" mb={4}>Próximos Passos</Heading>
                        <VStack align="stretch" spacing={4}>
                            <HStack p={4} bg="gray.50" borderRadius="xl" cursor="pointer" transition="0.2s" _hover={{bg: "pink.50"}}>
                                <Icon as={Plus} color="pink.500" />
                                <Box><Text fontWeight="bold">Tire uma foto do pedido</Text><Text fontSize="xs" color="gray.500">A Bella extrai os produtos automaticamente.</Text></Box>
                            </HStack>
                            <HStack p={4} bg="gray.50" borderRadius="xl" cursor="pointer" transition="0.2s" _hover={{bg: "blue.50"}}>
                                <Icon as={Users} color="blue.500" />
                                <Box><Text fontWeight="bold">Cadastre novos clientes</Text><Text fontSize="xs" color="gray.500">Mantenha sua base de contatos organizada.</Text></Box>
                            </HStack>
                        </VStack>
                    </GlassCard>
                    <GlassCard>
                        <Heading size="md" mb={4}>Performance Semanal</Heading>
                        <Box h="150px" bg="gray.50" borderRadius="xl" display="flex" alignItems="center" justifyContent="center">
                            <Text color="gray.400" fontSize="sm">Gráfico de desempenho indisponível no momento.</Text>
                        </Box>
                    </GlassCard>
                </SimpleGrid>
            </Stack>
        </Container>
    )
}

function AdminBackstage() {
    const [stats, setStats] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [activeTab, setActiveTab] = useState("dashboard")

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await axios.get(`${API_BASE}/admin/stats`)
                setStats(res.data)
            } catch (error) {
                console.error("Failed to fetch admin stats")
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    const renderHeader = () => (
        <Flex justify="space-between" align="center" mb={10}>
            <Box>
                <Badge colorScheme="red" mb={2} px={3} borderRadius="full">Super Admin Control</Badge>
                <Heading size="lg" fontFamily="Playfair Display">Bem-vindo ao Backstage</Heading>
            </Box>
            <HStack spacing={4}>
                <Button leftIcon={<RefreshCcw size={18} />} variant="outline" size="sm" onClick={() => window.location.reload()}>Recarregar Painel</Button>
                <Avatar size="md" name="Admin" src="https://bit.ly/broken-link" bg="red.600" />
            </HStack>
        </Flex>
    )

    const renderStats = () => (
        <SimpleGrid columns={{ base: 2, md: 4 }} spacing={6} mb={10}>
             <GlassCard p={4}><Stat><StatLabel fontSize="xs" color="gray.500">Representantes</StatLabel><StatNumber fontSize="2xl">{stats?.total_revendedoras ?? "0"}</StatNumber></Stat></GlassCard>
             <GlassCard p={4}><Stat><StatLabel fontSize="xs" color="gray.500">GMV (Mês)</StatLabel><StatNumber fontSize="2xl">R$ {stats?.vendas_mensais?.toLocaleString('pt-BR') ?? "0,00"}</StatNumber></Stat></GlassCard>
             <GlassCard p={4}><Stat><StatLabel fontSize="xs" color="gray.500">MRR</StatLabel><StatNumber fontSize="2xl">R$ {stats?.mrr?.toLocaleString('pt-BR') ?? "0,00"}</StatNumber></Stat></GlassCard>
             <GlassCard p={4}><Stat><StatLabel fontSize="xs" color="gray.500">Status IA</StatLabel><StatNumber fontSize="2xl" color="green.500">{stats?.llm_status ?? "OK"}</StatNumber></Stat></GlassCard>
        </SimpleGrid>
    )

    return (
        <Container maxW="container.xl" py={8}>
            {renderHeader()}
            
            <HStack spacing={6} mb={8} borderBottom="1px solid" borderColor="gray.100" pb={4} overflowX="auto">
                <Button variant="link" color={activeTab === 'dashboard' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('dashboard')} leftIcon={<LayoutDashboard size={18}/>}>Dashboard</Button>
                <Button variant="link" color={activeTab === 'representantes' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('representantes')} leftIcon={<Users size={18}/>}>Representantes</Button>
                <Button variant="link" color={activeTab === 'ia' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('ia')} leftIcon={<Cpu size={18}/>}>Agentes IA</Button>
                <Button variant="link" color={activeTab === 'infra' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('infra')} leftIcon={<Server size={18}/>}>Infra & LLM</Button>
                <Button variant="link" color={activeTab === 'db' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('db')} leftIcon={<Database size={18}/>}>Explorador BD</Button>
                <Button variant="link" color={activeTab === 'settings' ? 'pink.500' : 'gray.500'} onClick={() => setActiveTab('settings')} leftIcon={<Settings size={18}/>}>Ajustes</Button>
            </HStack>

            {activeTab === 'dashboard' && (
                <Stack spacing={8}>
                    {renderStats()}
                    <Grid templateColumns={{ base: "1fr", md: "2fr 1fr" }} gap={8}>
                        <GridItem><AdminRevendedoras /></GridItem>
                        <GridItem><VStack align="stretch" spacing={6}><ProductUpload /><AdminAnalytics/></VStack></GridItem>
                    </Grid>
                </Stack>
            )}

            {activeTab === 'representantes' && <AdminRevendedoras />}
            {activeTab === 'ia' && <AdminAgents />}
            {activeTab === 'infra' && <AdminLLMManager />}
            {activeTab === 'db' && <AdminDBExplorer />}
            {activeTab === 'settings' && <AdminSettings />}
        </Container>
    )
}

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [isAdmin, setIsAdmin] = useState(false)
    const navigate = useNavigate(); const location = useLocation()
    const isAdminPath = location.pathname.startsWith('/backstage')

    if (!isAuthenticated && !isAdminPath) return <Login onLogin={() => { setIsAuthenticated(true); navigate('/'); }} />
    if (isAdminPath && !isAdmin) return <AdminLogin onLogin={() => { setIsAdmin(true); setIsAuthenticated(true); navigate('/backstage'); }} />

    return (
        <Box minH="100vh" bg="gray.50">
            <Flex as="nav" bg={isAdmin ? "gray.900" : "white"} color={isAdmin ? "white" : "inherit"} height="80px" px={8} position="sticky" top={0} zIndex={100} shadow="sm" justify="space-between" align="center">
                <Stack direction="row" align="center" spacing={2} cursor="pointer" onClick={() => navigate('/')}>
                    <Icon as={Sparkles} color="pink.500" w={6} h={6} />
                    <Heading size="md" fontWeight="800">BellaZap</Heading>
                    {isAdmin && <Badge colorScheme="red" ml={2}>ADMIN</Badge>}
                </Stack>
                <Stack direction="row" spacing={8} display={{ base: "none", md: "flex" }}>
                    {!isAdmin ? (
                        <>
                            <Button as={Link} to="/" variant="link" color="pink.500" leftIcon={<LayoutDashboard size={18} />}>Dashboard</Button>
                            <Button variant="link" color="gray.500" leftIcon={<ShoppingBag size={18} />}>Produtos</Button>
                            <Button variant="link" color="gray.500" leftIcon={<Wallet size={18} />}>Finanças</Button>
                        </>
                    ) : (
                        <>
                            <Button as={Link} to="/backstage" variant="link" color="white" leftIcon={<ShieldCheck size={18} />}>Central de Comando</Button>
                        </>
                    )}
                </Stack>
                <Menu>
                    <MenuButton>
                        <Avatar size="sm" name={isAdmin ? "Super Admin" : "Bella User"} bg={isAdmin ? "red.600" : "pink.500"} />
                    </MenuButton>
                    <MenuList color="gray.800">
                        <MenuItem icon={<LogOut size={16} />} onClick={() => { setIsAuthenticated(false); setIsAdmin(false); navigate('/'); }}>Sair</MenuItem>
                    </MenuList>
                </Menu>
            </Flex>
            <Box as="main">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/backstage/*" element={<AdminBackstage />} />
                </Routes>
            </Box>
        </Box>
    )
}

export default App
