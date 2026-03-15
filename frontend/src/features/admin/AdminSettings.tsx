import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, Box, Grid, Button,
    FormControl, FormLabel, Select, Input, useToast,
    Stack, Icon, Accordion, AccordionItem, AccordionButton,
    AccordionPanel, AccordionIcon, HStack, Progress, Skeleton
} from '@chakra-ui/react';
import { FileText, Server, Zap, Database, HelpCircle, RefreshCcw, Activity } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

// --- Sub-components ---

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

function HelpAccordion({ topic }: { topic: string }) {
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(false);

    const fetchHelp = async () => {
        if (content) return;
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/admin/help/${topic}`);
            setContent(res.data.content);
        } catch (e) {
            setContent("Falha ao carregar o guia. Verifique se o arquivo existe no backend.");
        } finally {
            setLoading(false);
        }
    };

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
    );
}

// --- Main component ---

export default function AdminSettings() {
    const [activeTab, setActiveTab] = useState("help");
    const [configs, setConfigs] = useState<any[] | null>(null);
    const [loadingConfigs, setLoadingConfigs] = useState(true);
    const [loadingAction, setLoadingAction] = useState(false);
    const toast = useToast();

    const loadConfigs = async () => {
        setLoadingConfigs(true);
        try {
            const { data } = await axios.get(`${API_BASE}/admin/configs`);
            setConfigs(data);
        } catch (e) {
            toast({ title: "Erro ao carregar configurações", status: "error" });
            setConfigs([]);
        } finally {
            setLoadingConfigs(false);
        }
    };

    useEffect(() => { loadConfigs() }, []);

    const updateConfig = (key: string, value: string, category: string) => {
        axios.post(`${API_BASE}/admin/configs`, { key, value, category })
            .then(() => {
                toast({ title: "Salvo", status: "success", duration: 1500 });
                if (configs) {
                    const newConfigs = [...configs];
                    const index = newConfigs.findIndex(c => c.key === key);
                    if (index > -1) newConfigs[index].value = value;
                    else newConfigs.push({ key, value, category });
                    setConfigs(newConfigs);
                }
            })
            .catch(() => toast({ title: "Erro ao salvar", status: "error" }));
    };
    
    const getConfig = (key: string) => configs?.find(c => c.key === key)?.value || "";

    const GlassCard = ({ children, ...props }: any) => (
        <Box bg="white" borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100" p={6} {...props}>
            {children}
        </Box>
    );

    const renderForms = () => {
        if (loadingConfigs) return <Stack><Skeleton h="150px" borderRadius="2xl"/><Skeleton h="80px" borderRadius="2xl"/></Stack>;
        
        return (
            <>
                {activeTab === "infra" && (
                    <Stack spacing={6}>
                        <GlassCard>
                            <Heading size="sm" mb={6}>Manual LLM Fallback</Heading>
                            <Stack spacing={4}>
                                <FormControl><FormLabel>Provedor</FormLabel><Select value={getConfig('fallback_provider')} onChange={(e) => updateConfig('fallback_provider', e.target.value, 'llm')}><option value="openai">OpenAI</option><option value="google">Google (Gemini Pro)</option><option value="groq">Groq (Llama-3)</option></Select></FormControl>
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

                {activeTab === "help" && (
                     <GlassCard>
                        <Heading size="md" mb={4}>Central de Orientações</Heading>
                        <Text color="gray.600" mb={6}>Guias práticos para gestão da plataforma.</Text>
                        <Accordion allowMultiple>
                            <StaticHelpAccordion title="Configuração WhatsApp" content={<Text>A Evolution API conecta a BellaZap ao seu número. Use a aba correspondente para salvar suas credenciais.</Text>}/>
                            <StaticHelpAccordion title="Pagamentos Asaas" content={<Text>A integração financeira é processada via Asaas. O split é configurado automaticamente no cadastro.</Text>}/>
                        </Accordion>
                    </GlassCard>
                )}
            </>
        );
    };

    return (
        <VStack align="stretch" spacing={6}>
            <Heading size="md">Ajustes & Documentação</Heading>
            <Grid templateColumns={{ base: "1fr", md: "250px 1fr" }} gap={8}>
                <VStack align="start" spacing={2}>
                    <Button variant={activeTab === "help" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<FileText size={18} />} onClick={() => setActiveTab("help")}>Central de Ajuda</Button>
                    <Button variant={activeTab === "infra" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Server size={18} />} onClick={() => setActiveTab("infra")}>Fallback & LLM</Button>
                    <Button variant={activeTab === "evo" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Zap size={18} />} onClick={() => setActiveTab("evo")}>Evolution API</Button>
                </VStack>
                <Box>{renderForms()}</Box>
            </Grid>
        </VStack>
    );
}
