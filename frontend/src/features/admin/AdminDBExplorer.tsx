import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, Box, Select, Table, Thead, Tbody,
    Tr, Th, Td, TableContainer, Skeleton, HStack, Badge,
    IconButton, useToast, Center, Icon
} from '@chakra-ui/react';
import { Database, RefreshCcw, Search, Info } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

export default function AdminDBExplorer() {
    const [table, setTable] = useState("revendedoras");
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const toast = useToast();

    const fetchTableData = async () => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/admin/db/explorer/${table}`);
            setData(res.data);
        } catch (e) {
            toast({ title: "Erro ao explorar tabela", status: "error" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTableData();
    }, [table]);

    const getColumns = () => {
        if (data.length === 0) return [];
        return Object.keys(data[0]);
    }

    return (
        <VStack align="stretch" spacing={6}>
            <HStack justify="space-between">
                <Box>
                    <Heading size="md">Data Explorer</Heading>
                    <Text color="gray.500" fontSize="sm">Acesso direto e seguro às tabelas do banco de dados.</Text>
                </Box>
                <HStack spacing={4}>
                    <Select 
                        w="200px" 
                        value={table} 
                        onChange={(e) => setTable(e.target.value)}
                        bg="white"
                    >
                        <option value="revendedoras">Representantes</option>
                        <option value="vendas">Vendas</option>
                        <option value="produtos">Catálogo Global</option>
                        <option value="transactions">Transações Financeiras</option>
                        <option value="logs">Logs de IA</option>
                    </Select>
                    <IconButton 
                        aria-label="Refresh" 
                        icon={<RefreshCcw size={18} />} 
                        onClick={fetchTableData}
                        isLoading={loading}
                    />
                </HStack>
            </HStack>

            <Box bg="white" p={4} borderRadius="2xl" border="1px solid" borderColor="gray.100" shadow="sm">
                {loading ? <Skeleton h="400px" borderRadius="xl" /> : data.length > 0 ? (
                    <TableContainer maxH="600px" overflowY="auto">
                        <Table variant="simple" size="sm">
                            <Thead position="sticky" top={0} bg="white" zIndex={1}>
                                <Tr>
                                    {getColumns().map(col => (
                                        <Th key={col} whiteSpace="nowrap">{col.replace('_', ' ')}</Th>
                                    ))}
                                </Tr>
                            </Thead>
                            <Tbody>
                                {data.map((row, i) => (
                                    <Tr key={i} _hover={{ bg: "gray.50" }}>
                                        {getColumns().map(col => (
                                            <Td key={col} maxW="200px" overflow="hidden" textOverflow="ellipsis" whiteSpace="nowrap">
                                                {typeof row[col] === 'boolean' ? (
                                                    <Badge colorScheme={row[col] ? "green" : "red"}>{row[col] ? "True" : "False"}</Badge>
                                                ) : (
                                                    String(row[col] ?? "—")
                                                )}
                                            </Td>
                                        ))}
                                    </Tr>
                                ))}
                            </Tbody>
                        </Table>
                    </TableContainer>
                ) : (
                    <Center p={10} flexDirection="column">
                        <Icon as={Info} w={10} h={10} color="gray.300" mb={4} />
                        <Text color="gray.500">Nenhum dado encontrado para esta tabela.</Text>
                    </Center>
                )}
            </Box>
        </VStack>
    );
}
