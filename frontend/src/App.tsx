import React, { useState, useEffect, useRef } from 'react'
import { Routes, Route, useNavigate, useLocation, Link } from 'react-router-dom'
import {
    Box,
    Flex,
    Heading,
    Button,
    Stack,
    Text,
    Container,
    Grid,
    GridItem,
    Icon,
    Avatar,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
    Badge,
    useToast,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    FormControl,
    FormLabel,
    Input,
    Select,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    useDisclosure,
    Divider,
    HStack,
    Progress,
    IconButton,
    Textarea,
    Switch,
    Tabs,
    TabList,
    TabPanels,
    Tab,
    TabPanel,
    VStack,
    SimpleGrid,
    NumberInput,
    NumberInputField,
    Alert,
    AlertIcon,
    Skeleton,
    Accordion,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon,
    Center
} from '@chakra-ui/react'
import {
    LayoutDashboard,
    ShoppingBag,
    Wallet,
    LogOut,
    ChevronRight,
    Bell,
    Sparkles,
    Settings,
    Users,
    ArrowUpRight,
    Plus,
    Eye,
    Cpu,
    TrendingUp,
    CreditCard,
    MessageSquare,
    Activity,
    ShieldCheck,
    Server,
    Database,
    RefreshCcw,
    Upload,
    Zap,
    Lock,
    HardDrive,
    Bot,
    Trash2,
    HelpCircle,
    FileText,
    Info
} from 'lucide-react'
import axios from 'axios'
import Login from './features/auth/Login'
import AdminLogin from './features/auth/AdminLogin'

const API_BASE = "http://localhost:8000/api/v1"

const GlassCard = ({ children, ...props }: any) => (
    <Box bg="white" borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100" p={6} transition="all 0.3s" _hover={{ shadow: 'md', transform: 'translateY(-2px)' }} {...props}>
        {children}
    </Box>
)

// --- Static Help Component ---
const StaticHelpAccordion = ({ title, content }: { title: string, content: React.ReactNode }) => (
    <AccordionItem border="none" mb={2}>
        <AccordionButton bg="gray.50" borderRadius="xl" _expanded={{ bg: "pink.50", color: "pink.700" }}>
            <Box flex="1" textAlign="left" fontWeight="bold">
                <HStack><Icon as={HelpCircle} size={18} /><Text>{title}</Text></HStack>
            </Box>
            <AccordionIcon />
        </AccordionButton>
        <AccordionPanel pb={4} fontSize="sm">
            {content}
        </AccordionPanel>
    </AccordionItem>
);


// --- Components ---

function HelpAccordion({ topic }: { topic: string }) {
    const [content, setContent] = useState("")
    const [loading, setLoading] = useState(false)

    const fetchHelp = async () => {
        if (content) return
        setLoading(true)
        try {
            const res = await axios.get(`${API_BASE}/admin/help/${topic}`)
            setContent(res.data.content)
        } catch (e) {
            setContent("Falha ao carregar o guia. Verifique se o arquivo existe no backend.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <AccordionItem border="none" mb={2}>
            <AccordionButton bg="gray.50" borderRadius="xl" _expanded={{ bg: "pink.50", color: "pink.700" }} onClick={fetchHelp}>
                <Box flex="1" textAlign="left" fontWeight="bold">
                    <HStack><Icon as={HelpCircle} size={18} /><Text>Como configurar {topic.toUpperCase()}?</Text></HStack>
                </Box>
                <AccordionIcon />
            </AccordionButton>
            <AccordionPanel pb={4} fontSize="sm">
                {loading ? <Progress size="xs" isIndeterminate colorScheme="pink" /> : <Box whiteSpace="pre-wrap">{content}</Box>}
            </AccordionPanel>
        </AccordionItem>
    )
}

function CreateEditAgentModal({ isOpen, onClose, onSaved, agent }: any) {
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({ nome: '', departamento: 'vendas', prompt_contexto: '', model_name: 'qwen2.5:3b', is_active: true })
    const toast = useToast()

    useEffect(() => {
        if (agent) setFormData(agent)
        else setFormData({ nome: '', departamento: 'vendas', prompt_contexto: '', model_name: 'qwen2.5:3b', is_active: true })
    }, [agent, isOpen])

    const handleSubmit = async () => {
        setLoading(true)
        try {
            if (agent?.id) await axios.put(`${API_BASE}/admin/agents/${agent.id}`, formData)
            else await axios.post(`${API_BASE}/admin/agents`, formData)
            toast({ title: "Agente Salvo", status: "success" })
            onSaved()
            onClose()
        } catch (e) {
            toast({ title: "Erro ao salvar", status: "error" })
        } finally {
            setLoading(false)
        }
    }

    return (
        <Modal isOpen={isOpen} onClose={onClose} size="xl">
            <ModalOverlay />
            <ModalContent borderRadius="2xl">
                <ModalHeader>{agent ? "Editar Agente" : "Novo Agente IA"}</ModalHeader>
                <ModalCloseButton />
                <ModalBody pb={6}>
                    <Stack spacing={4}>
                        <FormControl isRequired><FormLabel>Nome do Agente</FormLabel><Input value={formData.nome} onChange={(e) => setFormData({ ...formData, nome: e.target.value })} /></FormControl>
                        <FormControl isRequired><FormLabel>Departamento</FormLabel><Select value={formData.departamento} onChange={(e) => setFormData({ ...formData, departamento: e.target.value })}><option value="vendas">Vendas</option><option value="suporte">Suporte</option><option value="financeiro">Financeiro</option></Select></FormControl>
                        <FormControl isRequired><FormLabel>Prompt Estratégico</FormLabel><Textarea rows={6} value={formData.prompt_contexto} onChange={(e) => setFormData({ ...formData, prompt_contexto: e.target.value })} /></FormControl>
                        <FormControl><FormLabel>Modelo Preferencial</FormLabel><Input value={formData.model_name} onChange={(e) => setFormData({ ...formData, model_name: e.target.value })} /></FormControl>
                        <FormControl display="flex" alignItems="center"><FormLabel mb="0">Ativo</FormLabel><Switch isChecked={formData.is_active} onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} /></FormControl>
                    </Stack>
                </ModalBody>
                <ModalFooter><Button colorScheme="pink" mr={3} isLoading={loading} onClick={handleSubmit}>Salvar Persona</Button><Button onClick={onClose}>Cancelar</Button></ModalFooter>
            </ModalContent>
        </Modal>
    )
}

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
                Use esta ferramenta para enviar uma nova lista de produtos para a plataforma. O arquivo deve ser no formato <strong>.CSV</strong> e seguir a estrutura correta de colunas.
            </Text>
            <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={handleUpload} accept=".csv" />
            <Button leftIcon={<Upload size={18} />} variant="outline" colorScheme="pink" isLoading={loading} onClick={() => fileInputRef.current?.click()}>
                Importar Planilha de Produtos (.CSV)
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
                    <Button leftIcon={<Bell size={18} />} variant="ghost" borderRadius="full">Notificações</Button>
                </Flex>
                <Grid templateColumns={{ base: "repeat(1, 1fr)", md: "repeat(3, 1fr)" }} gap={6}>
                    <GridItem><GlassCard><Stat><StatLabel color="gray.500" textTransform="uppercase" fontSize="xs">Saldo Disponível</StatLabel><StatNumber fontSize="3xl" color="pink.500">R$ 1.250,00</StatNumber><StatHelpText>Split ativo (8%)</StatHelpText></Stat></GlassCard></GridItem>
                    <GridItem><GlassCard><Stat><StatLabel color="gray.500" textTransform="uppercase" fontSize="xs">Vendas do Mês</StatLabel><StatNumber fontSize="3xl">32 / 100</StatNumber><StatHelpText>Plano Bella Pro</StatHelpText></Stat></GlassCard></GridItem>
                    <GridItem><Box p={6} bg="orange.400" color="white" borderRadius="2xl" shadow="xl"><Stat><StatLabel opacity={0.8} textTransform="uppercase" fontSize="xs">Lançamento</StatLabel><StatNumber fontSize="2xl">Natura Una Gold</StatNumber><StatHelpText opacity={0.8}>Disponível 24/02</StatHelpText></Stat></Box></GridItem>
                </Grid>
            </Stack>
        </Container>
    )
}

function AdminDashboard() {
    const [stats, setStats] = useState<any>(null)
    const [revendedoras, setRevendedoras] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true)
            try {
                const [statsRes, revendedorasRes] = await Promise.all([
                    axios.get(`${API_BASE}/admin/stats`),
                    axios.get(`${API_BASE}/admin/revendedoras`)
                ])
                setStats(statsRes.data)
                setRevendedoras(revendedorasRes.data)
            } catch (error) {
                console.error("Failed to fetch admin data", error)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    const renderStatCard = (label: string, value: string | number, color?: string) => (
        <GlassCard>
            <Stat>
                <StatLabel fontSize="xs">{label}</StatLabel>
                <StatNumber color={color}>{value}</StatNumber>
            </Stat>
        </GlassCard>
    );

    return (
        <Container maxW="container.xl" py={8}>
            <Stack spacing={8}>
                <Flex justify="space-between" align="center">
                    <Box><Badge colorScheme="red" mb={2} px={3} borderRadius="full">Super Admin</Badge><Heading size="lg" fontFamily="Playfair Display">Dashboard Global</Heading></Box>
                </Flex>
                
                {loading ? (
                    <SimpleGrid columns={{ base: 2, md: 4 }} spacing={6}>
                        <Skeleton h="100px" borderRadius="2xl" /><Skeleton h="100px" borderRadius="2xl" /><Skeleton h="100px" borderRadius="2xl" /><Skeleton h="100px" borderRadius="2xl" />
                    </SimpleGrid>
                ) : (
                    <SimpleGrid columns={{ base: 2, md: 4 }} spacing={6}>
                        {renderStatCard("Revendedoras", stats?.total_revendedoras ?? "0")}
                        {renderStatCard("GMV Confirmado", `R$ ${stats?.vendas_mensais?.toLocaleString('pt-BR') ?? "0,00"}`)}
                        {renderStatCard("Recorrência (MRR)", `R$ ${stats?.mrr?.toLocaleString('pt-BR') ?? "0,00"}`)}
                        {renderStatCard("Latency IA", stats?.llm_status ?? "N/A", "green.500")}
                    </SimpleGrid>
                )}
                
                <Grid templateColumns={{ base: "1fr", md: "2fr 1fr" }} gap={8}>
                    <GridItem>
                        <GlassCard>
                            <Heading size="md" mb={6}>Gestão de Representantes</Heading>
                            {loading ? <Skeleton h="150px" borderRadius="lg" /> : (
                            <TableContainer>
                                <Table variant="simple">
                                    <Thead><Tr><Th>Representante</Th><Th>WhatsApp</Th><Th>Plano</Th><Th>Ações</Th></Tr></Thead>
                                    <Tbody>
                                        {revendedoras.length > 0 ? revendedoras.map(r => (
                                            <Tr key={r.id}><Td fontWeight="600">{r.nome}</Td><Td>{r.telefone}</Td><Td><Badge colorScheme="pink">{r.plano}</Badge></Td><Td><IconButton aria-label="Ver" icon={<Eye size={18} />} size="sm" variant="ghost" /></Td></Tr>
                                        )) : (
                                            <Tr><Td colSpan={4} textAlign="center"><Text color="gray.500">Nenhuma revendedora encontrada.</Text></Td></Tr>
                                        )}
                                    </Tbody>
                                </Table>
                            </TableContainer>
                             )}
                        </GlassCard>
                    </GridItem>
                    <GridItem>
                        <ProductUpload />
                    </GridItem>
                </Grid>
            </Stack>
        </Container>
    )
}

function AgentsView() {
    const [agents, setAgents] = useState<any[]>([])
    const [logs, setLogs] = useState<any[]>([])
    const [selectedAgent, setSelectedAgent] = useState<any>(null)
    const { isOpen, onOpen, onClose } = useDisclosure()
    const toast = useToast()

    const refresh = () => {
        axios.get(`${API_BASE}/admin/agents`).then(res => setAgents(res.data))
        axios.get(`${API_BASE}/admin/agents/logs`).then(res => setLogs(res.data))
    }
    useEffect(() => { refresh() }, [])

    const deleteAgent = async (id: string) => {
        if (!confirm("Remover esta persona?")) return
        try { await axios.delete(`${API_BASE}/admin/agents/${id}`); toast({ title: "Removido", status: "success" }); refresh(); } catch (e) { }
    }

    return (
        <Container maxW="container.xl" py={8}>
            <Stack spacing={8}>
                <Flex justify="space-between" align="center">
                    <Box><Heading size="lg" fontFamily="Playfair Display">IA & Orquestração</Heading><Text color="gray.500">Modele as personas de IA da plataforma.</Text></Box>
                    <Button leftIcon={<Plus size={18} />} colorScheme="red" onClick={() => { setSelectedAgent(null); onOpen(); }}>Nova Persona</Button>
                </Flex>

                <Tabs variant="soft-rounded" colorScheme="pink">
                    <TabList bg="white" p={1} borderRadius="full" w="fit-content"><Tab leftIcon={<Bot size={18} />}>Personas Ativas</Tab><Tab leftIcon={<MessageSquare size={18} />}>Audit Log</Tab></TabList>
                    <TabPanels>
                        <TabPanel px={0}>
                            <SimpleGrid columns={{ base: 1, md: 3 }} gap={6}>
                                {agents.map(a => (
                                    <GlassCard key={a.id}>
                                        <VStack align="start" spacing={4}>
                                            <HStack w="full" justify="space-between"><Badge colorScheme={a.is_active ? "green" : "gray"}>{a.is_active ? "On" : "Off"}</Badge><Badge variant="outline">{a.departamento}</Badge></HStack>
                                            <Box><Text fontWeight="bold" fontSize="lg">{a.nome}</Text><Text fontSize="xs" color="pink.500">{a.model_name}</Text></Box>
                                            <Text fontSize="sm" noOfLines={3} color="gray.600">"{a.prompt_contexto}"</Text>
                                            <HStack w="full"><Button size="sm" flex={1} variant="outline" onClick={() => { setSelectedAgent(a); onOpen(); }}>Editar</Button><IconButton aria-label="Delete" icon={<Trash2 size={16} />} size="sm" colorScheme="red" variant="ghost" onClick={() => deleteAgent(a.id)} /></HStack>
                                        </VStack>
                                    </GlassCard>
                                ))}
                            </SimpleGrid>
                        </TabPanel>
                        <TabPanel px={0}><GlassCard><Stack spacing={4}>{logs.map(l => (<Box key={l.id} p={3} bg="gray.50" borderRadius="lg"><HStack justify="space-between"><Badge colorScheme={l.role === 'assistant' ? 'pink' : 'gray'}>{l.role}</Badge><Text fontSize="xs" color="gray.400">{l.timestamp} | {l.model_used}</Text></HStack><Text mt={2} fontSize="sm">{l.content}</Text></Box>))}</Stack></GlassCard></TabPanel>
                    </TabPanels>
                </Tabs>
            </Stack>
            <CreateEditAgentModal isOpen={isOpen} onClose={onClose} onSaved={refresh} agent={selectedAgent} />
        </Container>
    )
}

function FinancialView() {
    const [analysis, setAnalysis] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    useEffect(() => {
        axios.get(`${API_BASE}/admin/financial/predictive`)
            .then(res => { setAnalysis(res.data) })
            .catch(err => console.error("Failed to fetch financial analysis", err))
            .finally(() => setLoading(false))
    }, [])

    const hasData = analysis && analysis.insights?.length > 0 && analysis.top_performers?.length > 0;

    return (
        <Container maxW="container.xl" py={8}>
            <Stack spacing={8}>
                <Heading size="lg" fontFamily="Playfair Display">Financial Brain</Heading>
                
                {loading ? (
                    <Grid templateColumns={{ base: "1fr", md: "2fr 1fr" }} gap={8}>
                        <Skeleton height="200px" borderRadius="2xl" />
                        <Skeleton height="200px" borderRadius="2xl" />
                    </Grid>
                ) : hasData ? (
                    <Grid templateColumns={{ base: "1fr", md: "2fr 1fr" }} gap={8}>
                        <Stack spacing={6}>
                            <GlassCard border="2px solid" borderColor="pink.100" bg="pink.50">
                                <Heading size="sm" mb={4} color="pink.700"><Icon as={TrendingUp} mr={2} /> Insights Bella IA</Heading>
                                <Stack spacing={3}>
                                    {analysis.insights.map((ins: string, i: number) => (<HStack key={i} p={3} bg="white" borderRadius="lg"><Icon as={ArrowUpRight} color="pink.500" /><Text fontWeight="600">{ins}</Text></HStack>))}
                                </Stack>
                            </GlassCard>
                        </Stack>
                        <GlassCard>
                            <Heading size="xs" mb={4} textTransform="uppercase">Top Performers</Heading>
                            <Stack spacing={3}>
                                {analysis.top_performers.map((n: string, i: number) => (
                                    <HStack key={i} justify="space-between">
                                        <Text fontWeight="bold">{n}</Text>
                                        <Badge colorScheme="blue"># {i + 1}</Badge>
                                    </HStack>
                                ))}
                            </Stack>
                        </GlassCard>
                    </Grid>
                ) : (
                    <GlassCard>
                        <Center flexDirection="column" p={8}>
                            <Icon as={Info} w={16} h={16} color="gray.300" mb={4} />
                            <Heading size="md" mb={2}>Nenhuma Análise Disponível</Heading>
                            <Text color="gray.600" textAlign="center">
                                Ainda não há dados suficientes para gerar uma análise preditiva. <br/>
                                Continue usando a plataforma para que a IA possa aprender e gerar insights.
                            </Text>
                        </Center>
                    </GlassCard>
                )}
            </Stack>
        </Container>
    )
}


function SettingsView() {
    const [activeTab, setActiveTab] = useState("help")
    const [configs, setConfigs] = useState<any[] | null>(null)
    const [loadingConfigs, setLoadingConfigs] = useState(true)
    const [loadingAction, setLoadingAction] = useState(false)
    const toast = useToast()

    const loadConfigs = async () => {
        setLoadingConfigs(true);
        try {
            const { data } = await axios.get(`${API_BASE}/admin/configs`);
            setConfigs(data);
        } catch (e) {
            toast({ title: "Erro ao carregar configurações", description: "Não foi possível buscar os ajustes do servidor.", status: "error" });
            setConfigs([]); // Set to empty array on failure to prevent breaking getConfig
        } finally {
            setLoadingConfigs(false);
        }
    }
    useEffect(() => { loadConfigs() }, [])

    const updateConfig = (key: string, value: string, category: string) => {
        axios.post(`${API_BASE}/admin/configs`, { key, value, category })
            .then(() => {
                toast({ title: "Salvo", status: "success", duration: 1500 });
                // Optimistic update
                if (configs) {
                    const newConfigs = [...configs];
                    const index = newConfigs.findIndex(c => c.key === key);
                    if (index > -1) newConfigs[index].value = value;
                    else newConfigs.push({ key, value, category });
                    setConfigs(newConfigs);
                }
            })
            .catch(() => toast({ title: "Erro ao salvar", status: "error" }));
    }
    
    const getConfig = (key: string) => configs?.find(c => c.key === key)?.value || ""

    const renderForms = () => {
        if (loadingConfigs) {
            return <Stack><Skeleton h="150px" borderRadius="2xl"/><Skeleton h="80px" borderRadius="2xl"/></Stack>
        }
        return (
            <>
                {activeTab === "infra" && (
                    <Stack spacing={6}>
                        <GlassCard>
                            <Heading size="sm" mb={6}>Manual LLM Fallback</Heading>
                            <Stack spacing={4}>
                                <FormControl><FormLabel>Provedor</FormLabel><Select value={getConfig('fallback_provider')} onChange={(e) => updateConfig('fallback_provider', e.target.value, 'llm')}><option value="openai">OpenAI</option><option value="google">Google (Gemini)</option><option value="groq">Groq (Llama-3)</option></Select></FormControl>
                                <FormControl><FormLabel>Modelo</FormLabel><Input placeholder="Ex: gemini-pro" defaultValue={getConfig('fallback_model')} onBlur={(e) => updateConfig('fallback_model', e.target.value, 'llm')} /></FormControl>
                                <FormControl><FormLabel>API Key</FormLabel><Input type="password" defaultValue={getConfig('fallback_key')} onBlur={(e) => updateConfig('fallback_key', e.target.value, 'llm')} /></FormControl>
                            </Stack>
                        </GlassCard>
                        <HelpAccordion topic="llm" />
                    </Stack>
                )}

                {activeTab === "evo" && (
                    <Stack spacing={6}>
                        <GlassCard>
                            <Heading size="sm" mb={6}>Evolution API</Heading>
                            <VStack spacing={4} align="start">
                                <FormControl><FormLabel>URL base</FormLabel><Input placeholder="https://..." defaultValue={getConfig('evo_url')} onBlur={(e) => updateConfig('evo_url', e.target.value, 'evolution')} /></FormControl>
                                <FormControl><FormLabel>API Key</FormLabel><Input type="password" defaultValue={getConfig('evo_key')} onBlur={(e) => updateConfig('evo_key', e.target.value, 'evolution')} /></FormControl>
                                <Button colorScheme="green" leftIcon={<RefreshCcw size={18} />} onClick={() => { setLoadingAction(true); axios.post(`${API_BASE}/admin/infra/evo/test`).then(res => { toast({ title: res.data.message, status: res.data.status === 'success' ? 'success' : 'error' }); setLoadingAction(false); }).catch(() => setLoadingAction(false)) }} isLoading={loadingAction}>Testar Conexão</Button>
                            </VStack>
                        </GlassCard>
                        <HelpAccordion topic="evolution" />
                    </Stack>
                )}

                {activeTab === "db" && (
                    <Stack spacing={6}>
                        <GlassCard>
                            <Heading size="sm" mb={4}>Manutenção Supabase</Heading>
                            <Button colorScheme="red" variant="outline" w="full" leftIcon={<Activity size={18} />} onClick={() => axios.post(`${API_BASE}/admin/infra/db/maintenance`).then(r => toast({ title: r.data.message, status: 'success' }))}>Rodar Otimização Manual</Button>
                        </GlassCard>
                        <HelpAccordion topic="supabase" />
                    </Stack>
                )}

                {activeTab === "help" && (
                     <GlassCard>
                        <Heading size="md" mb={4}>Central de Orientações</Heading>
                        <Text color="gray.600" mb={6}>Aqui você encontra guias passo a passo para configurar e usar as ferramentas da plataforma.</Text>
                        <Accordion allowMultiple>
                            <StaticHelpAccordion title="Como configurar a Evolution API?" content={
                                <Stack spacing={3}>
                                    <Text>A Evolution API é a ponte que conecta a BellaZap ao seu WhatsApp.</Text>
                                    <Text>1. Obtenha sua <strong>URL da API</strong> e sua <strong>API Key</strong> no seu painel da Evolution.</Text>
                                    <Text>2. Vá para a aba "Evolution API" aqui nos Ajustes.</Text>
                                    <Text>3. Insira a URL e a Chave nos campos correspondentes e salve.</Text>
                                    <Text>4. Clique em "Testar Conexão" para garantir que tudo está funcionando.</Text>
                                    <Button size="sm" variant="link" colorScheme="pink" onClick={() => setActiveTab("evo")}>Ir para a aba Evolution API</Button>
                                </Stack>
                            }/>
                            <StaticHelpAccordion title="Como funcionam os pagamentos (Asaas)?" content={
                                <Stack spacing={3}>
                                    <Text>Utilizamos a Asaas para processar os pagamentos das revendedoras. A integração é automática.</Text>
                                    <Text>Para visualizar seus pagamentos, acesse seu dashboard na Asaas.</Text>
                                    <Button as="a" href="https://www.asaas.com/" target="_blank" size="sm" variant="link" colorScheme="pink">Acessar Asaas</Button>
                                </Stack>
                            }/>
                            <StaticHelpAccordion title="O que é o LLM Fallback?" content={
                                <Text>
                                    O "LLM" é o nosso cérebro de Inteligência Artificial. Por padrão, usamos um modelo principal, mas se ele falhar, o sistema de "Fallback" entra em ação, usando um modelo secundário (como OpenAI ou Google) para que a plataforma nunca pare de funcionar. Você pode configurar qual modelo usar como secundário na aba "Fallback & LLM".
                                </Text>
                            }/>
                        </Accordion>
                    </GlassCard>
                )}
            </>
        )
    }

    return (
        <Container maxW="container.xl" py={8}>
            <Stack spacing={8}>
                <Heading size="lg" fontFamily="Playfair Display">Ajustes & Documentação</Heading>
                <Grid templateColumns={{ base: "1fr", md: "250px 1fr" }} gap={8}>
                    <VStack align="start" spacing={2}>
                        <Button variant={activeTab === "help" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<FileText size={18} />} onClick={() => setActiveTab("help")}>Central de Ajuda</Button>
                        <Button variant={activeTab === "infra" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Server size={18} />} onClick={() => setActiveTab("infra")}>Fallback & LLM</Button>
                        <Button variant={activeTab === "evo" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Zap size={18} />} onClick={() => setActiveTab("evo")}>Evolution API</Button>
                        <Button variant={activeTab === "db" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Database size={18} />} onClick={() => setActiveTab("db")}>Supabase / DB</Button>
                    </VStack>
                    <Box>{renderForms()}</Box>
                </Grid>
            </Stack>
        </Container>
    )
}

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [isAdmin, setIsAdmin] = useState(false)
    const navigate = useNavigate(); const location = useLocation()
    const isAdminPath = location.pathname.startsWith('/backstage')

    if (!isAuthenticated && !isAdminPath) return <Login onLogin={() => { setIsAuthenticated(true); navigate('/'); }} />
    if (isAdminPath && !isAdmin) return <AdminLogin onLogin={() => { setIsAdmin(true); setIsAuthenticated(true); navigate('/backstage/dashboard'); }} />

    return (
        <Box minH="100vh" bg="gray.50">
            <Flex as="nav" bg={isAdmin ? "dark.900" : "white"} color={isAdmin ? "white" : "inherit"} height="80px" px={8} position="sticky" top={0} zIndex={100} shadow="sm" justify="space-between" align="center">
                <Stack direction="row" align="center" spacing={2} cursor="pointer" onClick={() => navigate('/')}><Icon as={Sparkles} color="brand.500" w={6} h={6} /><Heading size="md" fontWeight="800">BellaZap</Heading>{isAdmin && <Badge colorScheme="red" ml={2}>ADMIN</Badge>}</Stack>
                <Stack direction="row" spacing={8} display={{ base: "none", md: "flex" }}>
                    {!isAdmin ? (<><Button as={Link} to="/" variant="link" color="brand.500" leftIcon={<LayoutDashboard size={18} />}>Dashboard</Button><Button variant="link" color="gray.500" leftIcon={<ShoppingBag size={18} />}>Produtos</Button><Button variant="link" color="gray.500" leftIcon={<Wallet size={18} />}>Finanças</Button></>) : (<><Button as={Link} to="/backstage/dashboard" variant="link" color={location.pathname === '/backstage/dashboard' ? "white" : "whiteAlpha.700"} leftIcon={<Users size={18} />}>Gestão</Button><Button as={Link} to="/backstage/agents" variant="link" color={location.pathname === '/backstage/agents' ? "white" : "whiteAlpha.700"} leftIcon={<Cpu size={18} />}>IA & Agentes</Button><Button as={Link} to="/backstage/financial" variant="link" color={location.pathname === '/backstage/financial' ? "white" : "whiteAlpha.700"} leftIcon={<TrendingUp size={18} />}>Analytics</Button><Button as={Link} to="/backstage/settings" variant="link" color={location.pathname === '/backstage/settings' ? "white" : "whiteAlpha.700"} leftIcon={<Settings size={18} />}>Ajustes</Button></>)}
                </Stack>
                <Menu><MenuButton><Avatar size="sm" name={isAdmin ? "Super Admin" : "Bella User"} bg={isAdmin ? "red.600" : "brand.500"} /></MenuButton><MenuList color="dark.900"><MenuItem icon={<LogOut size={16} />} onClick={() => { setIsAuthenticated(false); setIsAdmin(false); navigate('/'); }}>Sair</MenuItem></MenuList></Menu>
            </Flex>
            <Box as="main">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/backstage/dashboard" element={<AdminDashboard />} />
                    <Route path="/backstage/agents" element={<AgentsView />} />
                    <Route path="/backstage/financial" element={<FinancialView />} />
                    <Route path="/backstage/settings" element={<SettingsView />} />
                </Routes>
            </Box>
        </Box>
    )
}

export default App
