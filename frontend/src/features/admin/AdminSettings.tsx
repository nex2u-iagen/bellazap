import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, Box, Grid, Button,
    FormControl, FormLabel, Select, Input, useToast,
    Stack, Icon, Accordion, AccordionItem, AccordionButton,
    AccordionPanel, AccordionIcon, HStack, Progress, Skeleton
} from '@chakra-ui/react';
import { FileText, Server, Zap, Database, HelpCircle, RefreshCcw, Activity, MessageSquare } from 'lucide-react';
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
    const [configs, setConfigs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const toast = useToast();

    useEffect(() => {
        axios.get(`${API_BASE}/admin/configs`)
            .then(res => setConfigs(res.data))
            .catch(() => toast({ title: "Erro ao carregar configurações", status: "error" }))
            .finally(() => setLoading(false));
    }, []);

    const updateConfig = (key: string, value: string, category: string) => {
        axios.post(`${API_BASE}/admin/configs`, { key, value, category })
            .then(() => {
                toast({ title: "Salvo com sucesso!", status: "success", duration: 1500 });
                let newConfigs = [...configs];
                let idx = newConfigs.findIndex(c => c.key === key);
                if (idx > -1) newConfigs[idx].value = value;
                else newConfigs.push({ key, value, category });
                setConfigs(newConfigs);
            })
            .catch(() => toast({ title: "Erro ao salvar", status: "error" }));
    };

    const getConfig = (key: string) => configs.find(c => c.key === key)?.value || "";

    const GlassCard = ({ children, ...props }: any) => (
        <Box bg="white" borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100" p={6} {...props}>
            {children}
        </Box>
    );

    const renderForms = () => {
        if (loading) return <Skeleton h="300px" borderRadius="2xl" />;
        return (
            <>
                {activeTab === "infra" && (
                    <Stack spacing={6}>
                        <GlassCard>
                            <Heading size="sm" mb={6}>Configuração de LLM e Infraestrutura</Heading>
                            <Text color="gray.600" mb={4}>
                                As chaves de API (OpenAI, Groq, Gemini) agora são gerenciadas via variáveis de ambiente (.env) para maior segurança nativa na arquitetura Serverless (Vercel Edge).
                            </Text>
                            <Text fontSize="sm" color="gray.500">
                                Certifique-se de configurar <code>OPENAI_API_KEY</code> e <code>TURSO_DATABASE_URL</code> no ambiente de implantação.
                            </Text>
                        </GlassCard>
                    </Stack>
                )}

                {activeTab === "asaas" && (
                    <Stack spacing={6}>
                        <GlassCard borderTop="4px solid" borderColor="pink.500">
                            <Heading size="sm" mb={4}>Integração Asaas (Conta Master)</Heading>
                            <Text fontSize="sm" color="gray.600" mb={6}>
                                Configure sua chave API do Asaas e a Carteira (Wallet ID) principal. Essa conta receberá a taxa administrativa de todos os pagamentos da plataforma através do sistema de Split.
                            </Text>
                            
                            <Stack spacing={4}>
                                <FormControl>
                                    <FormLabel>Asaas API Key ($a_...)</FormLabel>
                                    <Input 
                                        type="password" 
                                        defaultValue={getConfig('asaas_api_key')}
                                        onBlur={(e) => updateConfig('asaas_api_key', e.target.value, 'asaas')}
                                        placeholder="Sua chave de API de Produção ou Sandbox" 
                                    />
                                </FormControl>
                                <FormControl>
                                    <FormLabel>Wallet ID Recebedor (Master)</FormLabel>
                                    <Input 
                                        defaultValue={getConfig('asaas_wallet_id')}
                                        onBlur={(e) => updateConfig('asaas_wallet_id', e.target.value, 'asaas')}
                                        placeholder="Ex: c7132a26-..." 
                                    />
                                    <Text fontSize="xs" color="gray.500" mt={1}>Você encontra sua Wallet ID nas configurações de 'Split de Pagamento' ou via API do Asaas.</Text>
                                </FormControl>
                                <FormControl>
                                    <FormLabel>Ambiente</FormLabel>
                                    <Select 
                                        value={getConfig('asaas_env') || "sandbox"}
                                        onChange={(e) => updateConfig('asaas_env', e.target.value, 'asaas')}
                                    >
                                        <option value="sandbox">Sandbox (Teste)</option>
                                        <option value="production">Produção</option>
                                    </Select>
                                </FormControl>
                            </Stack>
                        </GlassCard>
                    </Stack>
                )}

                {activeTab === "telegram" && (
                    <Stack spacing={6}>
                        <GlassCard borderTop="4px solid" borderColor="blue.500">
                            <Heading size="sm" mb={4}>Configuração do Bot Telegram</Heading>
                            <Text fontSize="sm" color="gray.600" mb={6}>
                                Informe o Token do seu Bot gerado pelo @BotFather. Este bot será o canal de atendimento oficial da BellaZap.
                            </Text>
                            
                            <Stack spacing={4}>
                                <FormControl>
                                    <FormLabel>Telegram Bot Token</FormLabel>
                                    <Input 
                                        type="password" 
                                        defaultValue={getConfig('telegram_bot_token')}
                                        onBlur={(e) => updateConfig('telegram_bot_token', e.target.value, 'telegram')}
                                        placeholder="Ex: 123456:ABC-DEF..." 
                                    />
                                </FormControl>
                                <FormControl>
                                    <FormLabel>Webhook Secret (Segurança)</FormLabel>
                                    <Input 
                                        defaultValue={getConfig('telegram_webhook_secret')}
                                        onBlur={(e) => updateConfig('telegram_webhook_secret', e.target.value, 'telegram')}
                                        placeholder="Um segredo aleatório para seu webhook" 
                                    />
                                    <Text fontSize="xs" color="gray.500" mt={1}>Este segredo é usado para garantir que apenas o Telegram envie mensagens para o seu backend.</Text>
                                </FormControl>
                                <Box p={4} bg="blue.50" borderRadius="xl">
                                    <Text fontSize="xs" fontWeight="bold" color="blue.700">Dica:</Text>
                                    <Text fontSize="xs" color="blue.600">
                                        Após trocar o token, lembre-se de atualizar a URL do Webhook no Telegram (ou via API) apontando para <code>sua-url.com/api/v1/telegram/webhook</code>.
                                    </Text>
                                </Box>
                            </Stack>
                        </GlassCard>
                    </Stack>
                )}

                {activeTab === "help" && (
                     <GlassCard>
                        <Heading size="md" mb={4}>Central de Orientações</Heading>
                        <Text color="gray.600" mb={6}>Guias práticos para gestão da plataforma.</Text>
                        <Accordion allowMultiple>
                            <StaticHelpAccordion title="Configuração Telegram" content={<Text>A integração com a cliente final ocorre via Telegram Bot. As revendedoras usam o comando /start com o email cadastrado para vincular a conta.</Text>}/>
                            <StaticHelpAccordion title="Split de Pagamentos Asaas" content={<Text>A conta Master recebe sua parte usando a Wallet ID configurada na aba Asaas. Cada representante deve ter sua conta Asaas ou Chave Pix para receber a parte dela.</Text>}/>
                            <StaticHelpAccordion title="Banco de Dados Turso" content={<Text>Os dados estão seguros no Turso (LibSQL). A visualização de tabelas e logs ocorre diretamente pelas ferramentas de CLI do Turso.</Text>}/>
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
                    <Button variant={activeTab === "telegram" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<MessageSquare size={18} />} onClick={() => setActiveTab("telegram")}>Bot Telegram</Button>
                    <Button variant={activeTab === "asaas" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Zap size={18} />} onClick={() => setActiveTab("asaas")}>Integração Asaas</Button>
                    <Button variant={activeTab === "infra" ? "solid" : "ghost"} colorScheme="pink" w="full" justifyContent="start" leftIcon={<Server size={18} />} onClick={() => setActiveTab("infra")}>Infra & Segurança</Button>
                </VStack>
                <Box>{renderForms()}</Box>
            </Grid>
        </VStack>
    );
}
