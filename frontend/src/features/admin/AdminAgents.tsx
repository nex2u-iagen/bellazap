import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, SimpleGrid, Box, Badge, 
    Icon, Button, useToast, HStack, IconButton,
    Tabs, TabList, TabPanels, Tab, TabPanel,
    useDisclosure, Skeleton
} from '@chakra-ui/react';
import { Bot, MessageSquare, Plus, Trash2, Edit3 } from 'lucide-react';
import axios from 'axios';
import CreateEditAgentModal from './CreateEditAgentModal';

const API_BASE = "http://localhost:8000/api/v1";

export default function AdminAgents() {
    const [agents, setAgents] = useState<any[]>([]);
    const [logs, setLogs] = useState<any[]>([]);
    const [selectedAgent, setSelectedAgent] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const toast = useToast();

    const fetchData = async () => {
        setLoading(true);
        try {
            const [agentsRes, logsRes] = await Promise.all([
                axios.get(`${API_BASE}/admin/agents`),
                axios.get(`${API_BASE}/admin/agents/logs`)
            ]);
            setAgents(agentsRes.data);
            setLogs(logsRes.data);
        } catch (error) {
            toast({ title: "Erro ao carregar agentes", status: "error" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const deleteAgent = async (id: string) => {
        if (!confirm("Remover esta persona?")) return;
        try {
            await axios.delete(`${API_BASE}/admin/agents/${id}`);
            toast({ title: "Removido", status: "success" });
            fetchData();
        } catch (e) {
            toast({ title: "Erro ao remover", status: "error" });
        }
    }

    const GlassCard = ({ children, ...props }: any) => (
        <Box bg="white" borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100" p={6} {...props}>
            {children}
        </Box>
    );

    return (
        <VStack align="stretch" spacing={8}>
            <HStack justify="space-between">
                <Box>
                    <Heading size="md">Personas & Agentes IA</Heading>
                    <Text color="gray.500" fontSize="sm">Defina o comportamento e o tom de voz da Bella.</Text>
                </Box>
                <Button 
                    leftIcon={<Plus size={18} />} 
                    colorScheme="pink" 
                    onClick={() => { setSelectedAgent(null); onOpen(); }}
                >
                    Nova Persona
                </Button>
            </HStack>

            <Tabs variant="soft-rounded" colorScheme="pink">
                <TabList mb={6}>
                    <Tab><HStack spacing={2}><Icon as={Bot} size={18} /><Text>Modelos Ativos</Text></HStack></Tab>
                    <Tab><HStack spacing={2}><Icon as={MessageSquare} size={18} /><Text>Logs de Auditoria</Text></HStack></Tab>
                </TabList>

                <TabPanels>
                    <TabPanel px={0}>
                        {loading ? (
                            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                                <Skeleton h="200px" borderRadius="2xl" /><Skeleton h="200px" borderRadius="2xl" /><Skeleton h="200px" borderRadius="2xl" />
                            </SimpleGrid>
                        ) : (
                            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                                {agents.map(a => (
                                    <GlassCard key={a.id}>
                                        <VStack align="start" spacing={4}>
                                            <HStack w="full" justify="space-between">
                                                <Badge colorScheme={a.is_active ? "green" : "gray"}>
                                                    {a.is_active ? "Ativo" : "Pausado"}
                                                </Badge>
                                                <Badge variant="outline" fontSize="xx-small">{a.departamento}</Badge>
                                            </HStack>
                                            <Box>
                                                <Text fontWeight="bold" fontSize="lg">{a.nome}</Text>
                                                <Text fontSize="xs" color="pink.500">{a.model_name}</Text>
                                            </Box>
                                            <Text fontSize="sm" noOfLines={3} color="gray.600">"{a.prompt_contexto}"</Text>
                                            <HStack w="full" pt={2}>
                                                <Button 
                                                    size="sm" 
                                                    flex={1} 
                                                    variant="outline" 
                                                    leftIcon={<Edit3 size={14} />}
                                                    onClick={() => { setSelectedAgent(a); onOpen(); }}
                                                >
                                                    Editar
                                                </Button>
                                                <IconButton 
                                                    aria-label="Delete" 
                                                    icon={<Trash2 size={16} />} 
                                                    size="sm" 
                                                    colorScheme="red" 
                                                    variant="ghost" 
                                                    onClick={() => deleteAgent(a.id)} 
                                                />
                                            </HStack>
                                        </VStack>
                                    </GlassCard>
                                ))}
                            </SimpleGrid>
                        )}
                    </TabPanel>

                    <TabPanel px={0}>
                        <GlassCard>
                            <VStack align="stretch" spacing={4}>
                                {logs.map(l => (
                                    <Box key={l.id} p={3} bg="gray.50" borderRadius="lg" borderLeft="4px solid" borderColor={l.role === 'assistant' ? 'pink.400' : 'blue.400'}>
                                        <HStack justify="space-between" mb={2}>
                                            <Badge colorScheme={l.role === 'assistant' ? 'pink' : 'blue'} fontSize="xs">
                                                {l.role}
                                            </Badge>
                                            <Text fontSize="xs" color="gray.400">{new Date(l.timestamp).toLocaleString()} | {l.model_used}</Text>
                                        </HStack>
                                        <Text fontSize="sm">{l.content}</Text>
                                    </Box>
                                ))}
                            </VStack>
                        </GlassCard>
                    </TabPanel>
                </TabPanels>
            </Tabs>

            <CreateEditAgentModal 
                isOpen={isOpen} 
                onClose={onClose} 
                onSaved={fetchData} 
                agent={selectedAgent} 
            />
        </VStack>
    );
}
