import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, SimpleGrid, Box, Badge, 
    Icon, Button, useToast, HStack, Progress, Stat,
    StatLabel, StatNumber, Divider, FormControl, FormLabel,
    Select, Input, Stack
} from '@chakra-ui/react';
import { Cpu, Zap, Activity, CheckCircle, XCircle, RefreshCcw } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

export default function AdminLLMManager() {
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [configs, setConfigs] = useState<any[]>([]);
    const toast = useToast();

    const checkHealth = async () => {
        setLoading(true);
        try {
            const res = await axios.post(`${API_BASE}/admin/infra/llm/check`);
            setStatus(res.data);
            toast({ title: "Status atualizado", status: "success", duration: 2000 });
        } catch (e) {
            toast({ title: "Erro ao validar LLMs", status: "error" });
        } finally {
            setLoading(false);
        }
    };

    const loadConfigs = async () => {
        try {
            const res = await axios.get(`${API_BASE}/admin/configs`);
            setConfigs(res.data.filter((c: any) => c.category === 'llm'));
        } catch (e) {}
    };

    useEffect(() => {
        checkHealth();
        loadConfigs();
    }, []);

    const updateConfig = async (key: string, value: string) => {
        try {
            await axios.post(`${API_BASE}/admin/configs`, { key, value, category: 'llm' });
            toast({ title: "Configuração salva", status: "success" });
            loadConfigs();
        } catch (e) {
            toast({ title: "Falha ao salvar", status: "error" });
        }
    }

    const getConfig = (key: string) => configs.find(c => c.key === key)?.value || "";

    const HealthCard = ({ provider, state, icon }: any) => (
        <Box p={5} bg="white" borderRadius="2xl" border="1px solid" borderColor="gray.100" shadow="sm">
            <HStack justify="space-between" mb={4}>
                <HStack>
                    <Icon as={icon} color="pink.500" />
                    <Text fontWeight="bold" textTransform="uppercase" fontSize="sm">{provider}</Text>
                </HStack>
                <Badge colorScheme={state === 'Online' || state === 'Configured' ? "green" : "red"} borderRadius="full" px={2}>
                    {state || "Desconhecido"}
                </Badge>
            </HStack>
            <Divider mb={4} />
            <Text fontSize="xs" color="gray.500">
                {state === 'Online' ? "Provider pronto para processar requisições localmente." : 
                 state === 'Configured' ? "Chave de API validada e pronta para uso em nuvem." :
                 "Verifique as configurações deste provider."}
            </Text>
        </Box>
    );

    return (
        <VStack align="stretch" spacing={8}>
            <HStack justify="space-between">
                <Box>
                    <Heading size="md">Inteligência & Orquestração</Heading>
                    <Text color="gray.500" fontSize="sm">Monitore o status dos modelos de linguagem.</Text>
                </Box>
                <Button 
                    leftIcon={<RefreshCcw size={18} />} 
                    variant="outline" 
                    colorScheme="pink" 
                    onClick={checkHealth}
                    isLoading={loading}
                >
                    Validar Conexões
                </Button>
            </HStack>

            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                <HealthCard provider="Ollama (Local)" state={status?.ollama} icon={Cpu} />
                <HealthCard provider="OpenAI (Cloud)" state={status?.openai} icon={Zap} />
                <HealthCard provider="Google Gemini" state="Em Teste" icon={Activity} />
            </SimpleGrid>

            <Box p={6} bg="white" borderRadius="2xl" border="1px solid" borderColor="gray.100" shadow="sm">
                <Heading size="sm" mb={6}>Configuração de Estratégia</Heading>
                <Stack spacing={6}>
                    <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
                        <FormControl>
                            <FormLabel>Provedor de Fallback</FormLabel>
                            <Select 
                                value={getConfig('fallback_provider')} 
                                onChange={(e) => updateConfig('fallback_provider', e.target.value)}
                            >
                                <option value="openai">OpenAI (GPT-4)</option>
                                <option value="google">Google (Gemini Pro)</option>
                                <option value="groq">Groq (Llama-3)</option>
                            </Select>
                        </FormControl>
                        <FormControl>
                            <FormLabel>Modelo Local</FormLabel>
                            <Input 
                                defaultValue={getConfig('local_model') || "qwen2.5:3b"} 
                                onBlur={(e) => updateConfig('local_model', e.target.value)} 
                            />
                        </FormControl>
                    </SimpleGrid>
                    
                    <Box p={4} bg="gray.50" borderRadius="xl">
                        <HStack justify="space-between" mb={2}>
                            <Text fontSize="sm" fontWeight="bold">Prioridade de Execução</Text>
                            <Badge colorScheme="purple">Auto-Scalable</Badge>
                        </HStack>
                        <Text fontSize="xs" color="gray.600">
                            O sistema prioriza o **Ollama (Local)** para reduzir custos. 
                            Em caso de latência superior a 15s ou erro de contexto, 
                            o fallback é acionado automaticamente.
                        </Text>
                    </Box>
                </Stack>
            </Box>
        </VStack>
    );
}
